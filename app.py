from flask import Flask, render_template, redirect, url_for, session, g, flash, Markup, request, make_response
from forms import RoomForm, ScheduleForm
from database import get_db, close_db
from flask_session import Session
from datetime import datetime
import time
from functools import wraps
from itertools import * 
from multiprocessing import Process, Value

from room import *
from house import House

user_house = House()
now = datetime.now().strftime("%H:%M")
outdoor_temp = user_house.outsideTemp.getCurrentOutsideTemp()

# BEST VIEWED ON PC/LAPTOP

app = Flask(__name__)
app.config["SECRET_KEY"] = "we-are-the-best"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('oh_no.html', title="Error"), 404

# Home page
@app.route("/")
def index():
    db = get_db()
    return render_template("index.html", title="Home", now=now)

# Shows terms and conditions
@app.route("/terms")
def terms():
    return render_template("terms_con.html", title="Terms and Conditions")

# Settings page
@app.route("/settings")
def settings():
    return render_template("settings.html", title="Settings")

# Profile page
@app.route("/profile")
def profile():
    return render_template("profile.html", title="My Profile")

# House page
@app.route("/house", methods=["GET", "POST"])
def house():
    form = RoomForm()
    rooms = None
    db = get_db()
    if form.validate_on_submit():
        automation = form.automation.data
        name = form.name.data
        
        db.execute("""INSERT INTO rooms (name, automation)
                        VALUES (?,?);""", (name, automation))
        db.commit()
        
        rooms = db.execute("""SELECT * FROM rooms WHERE room_id in 
                                (SELECT max(room_id) FROM rooms);""").fetchone()
        
        user_house.addNewRoom(int(rooms["room_id"]))
        
        flash ("Room successfully created! Add scheduling times below!")

        return redirect(url_for("room", id=rooms["room_id"]))
    else:
        rooms = db.execute("""SELECT * FROM rooms;""").fetchall()
    return render_template("house.html", form=form, title="Home", rooms=rooms, now=now, outdoor_temp=outdoor_temp)

# Edit Room page
@app.route("/edit_room/<int:id>", methods=["GET", "POST"])
def edit_room(id):
    form = RoomForm()
    room = None
    db = get_db()
    if form.validate_on_submit():
        automation = form.automation.data
        name = form.name.data
        
        db.execute("""UPDATE rooms SET name=?, automation=? WHERE room_id=?;""", (name, automation, id))
        db.commit()
        
        flash ("Room successfully updated!") 
        return redirect(url_for("room", id=id))
    else:
        room = db.execute("""SELECT * FROM rooms WHERE room_id=?;""", (id,)).fetchone()
    return render_template("edit_room.html", form=form, title="Edit Room", room=room, now=now)

# Deletes Room
@app.route("/delete_room/<int:id>")
def delete_room(id):
    db = get_db()
    db.execute("""DELETE FROM rooms WHERE room_id=?;""", (id,)).fetchone()
    db.commit()
    flash ("Room deleted!")
    return redirect(url_for("house"))

# Room Page
@app.route("/room/<int:id>", methods=["GET", "POST"])
def room(id):
    form = ScheduleForm()
    schedule = None
    db = get_db()
    room_id = id
    room = None
    correctRoomObject = user_house.getRoom(id)

    if form.validate_on_submit():
        desiredTemp = form.desiredTemp.data
        startTime = form.startTime.data
        endTime = form.endTime.data
        
        db.execute("""INSERT INTO schedules (room_id, desired_temp, start_time, end_time)
                        VALUES (?,?,?,?);""", (room_id, desiredTemp, startTime, endTime))
        db.commit()
        flash ("Schedule successfully added!")

        correctRoomObject.addToSchedule(str(startTime),int(desiredTemp),str(endTime))

        return redirect(url_for("room", id=room_id))
    else:
        schedule = db.execute("""SELECT * FROM schedules WHERE room_id=?;""", (room_id,)).fetchall()
        room = db.execute("""SELECT * FROM rooms WHERE room_id=?;""", (room_id,)).fetchone()
        current_temp = str(correctRoomObject.thermomstat.getCurrentTemp())

        #if correctRoomObject.roomSchedule.schedule:
            #correctRoomObject.scheduling()

        heater_state = "OFF"
        if correctRoomObject.heatingRunning == True:
            heater_state = "ON"

    return render_template("room.html", title="Room", schedule=schedule, form=form, room=room, now=now, current_temp=current_temp, outdoor_temp=outdoor_temp,heater_state=heater_state)

# Edit Schedule page
@app.route("/edit_schedule/<int:id>", methods=["GET", "POST"])
def edit_schedule(id):
    form = ScheduleForm()
    db = get_db()
    schedule = None
    if form.validate_on_submit():
        desiredTemp = form.desiredTemp.data
        startTime = form.startTime.data
        endTime = form.endTime.data
        
        db.execute("""UPDATE schedules SET desired_temp=?, start_time=?, end_time=? WHERE schedule_id=?;""", (desiredTemp, startTime, endTime, id))
        db.commit()

        schedule = db.execute("""SELECT * FROM schedules WHERE schedule_id=?;""", (id,)).fetchone()
        flash ("Schedule successfully updated!") 
        return redirect(url_for("room", id=schedule['room_id']))
    else:
        schedule = db.execute("""SELECT * FROM schedules WHERE schedule_id=?;""", (id,)).fetchone()
    return render_template("edit_schedule.html", form=form, title="Edit Schedule", schedule=schedule, now=now)

# Deletes Schedule
@app.route("/delete_schedule/<int:id>")
def delete_schedule(id):
    db = get_db()
    room_id =  db.execute("""SELECT room_id FROM schedules WHERE schedule_id=?;""", (id,)).fetchone()
    db.execute("""DELETE FROM schedules WHERE schedule_id=?;""", (id,)).fetchone()
    db.commit()
    flash ("Schedule deleted!")
    return redirect(url_for("room", id=int(room_id)))

def main(start):
    while True:
      if start.value == True:
        user_house.checkOutsideTempPeriodically()
        if user_house.rooms:
            for room in user_house.rooms:
                current = int(now[3] + now[4])
                if current > 1:
                    diff = current - 1
                    outOfRange = str(int(now[0] + now[1])+1) +':' +str(diff)
                else:
                    outOfRange = now[0]+now[1]+':' +str(current + 1)
                val1 =int(outOfRange[0]+outOfRange[1])
                if int(room.nextSchedule[0] +room.nextSchedule[1]) >= int(now[0]+now[1]) and int(room.nextSchedule[0] +room.nextSchedule[1]) <=int(outOfRange[0]+outOfRange[1]):
                    if int(room.nextSchedule[3] +room.nextSchedule[4]) >= int(now[3]+now[4]) and int(room.nextSchedule[3] +room.nextSchedule[4]) <=int(outOfRange[0]+outOfRange[1]):
                        print("before")
                        room.scheduling()
                        print("after")
                
                room.checkTempPeriodically(user_house.outsideTemp.getPreviousOutsideTemp(), user_house.outsideTemp.getCurrentOutsideTemp(), room.heaterPower)
        time.sleep(10)

if __name__ == '__main__':
    running = Value('b', True)
    p = Process(target=main, args=(running,))
    p.start()  
    app.run(debug=True)
    p.join()