from flask import Flask, render_template, redirect, url_for, session, g, flash, Markup, request, make_response
from forms import RoomForm, ScheduleForm, SettingForm
from database import get_db, close_db
from flask_session import Session
from datetime import datetime
from itertools import * 
from main import *
from threading import *

# BEST VIEWED ON PC/LAPTOP

outdoor_temp = user_house.outsideTemp.getCurrentOutsideTemp()

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

# Statistics page
@app.route("/statistics", methods=["GET", "POST"])
def statistics():
    form = SettingForm()
    if form.validate_on_submit():
        heatingAppliancePower = form.heatingAppliancePower.data
        energyLimit = form.energyLimit.data

        user_house.setHeatingPower(int(heatingAppliancePower))
        user_house.setMonthlyEnergyLimit(int(energyLimit))
        
        flash ("Settings updated!") 
        return redirect(url_for("statistics"))
    else:
        current_usage = str(user_house.getMonthlyEnergy())
        gauge = str(user_house.getEnergyHoursGuage())
        exceeded = str(user_house.getMonthlyEnergyExceeded())
        stats = user_house.getPastMonthStats()
        limit = str(user_house.getMonthlyEnergyLimit())
    return render_template("statistics.html", title="Statistics", current_usage=current_usage,gauge=gauge,stats=stats, limit=limit, exceeded=exceeded, form=form)

# House page
@app.route("/house", methods=["GET", "POST"])
def house():
    form = RoomForm()
    rooms = None
    db = get_db()
    if form.validate_on_submit():
        name = form.name.data
        
        db.execute("""INSERT INTO rooms (name) VALUES (?);""", (name,))
        db.commit()
        
        rooms = db.execute("""SELECT * FROM rooms WHERE room_id in 
                                (SELECT max(room_id) FROM rooms);""").fetchone()

        user_house.addNewRoom(int(rooms["room_id"]))

        flash ("Room successfully created! Add your scheduling times below!") 
        return redirect(url_for("room", id=rooms["room_id"]))
    else:
        rooms = db.execute("""SELECT * FROM rooms;""").fetchall()
    return render_template("house.html", form=form, title="Home", rooms=rooms, now=now, outdoor_temp=outdoor_temp)

# Room Page
@app.route("/room/<int:id>", methods=["GET", "POST"])
def room(id):
    form = ScheduleForm()
    schedule = None
    db = get_db()
    room_id = id
    room = None
    if form.validate_on_submit():
        desiredTemp = form.desiredTemp.data
        startTime = form.startTime.data
        endTime = form.endTime.data

        schedules = user_house.getRoom(room_id).getRoomSchedule()

        for key in schedules.keys():
            if startTime >= key and endTime <= schedules[key][1]:
                flash ('ERROR: Start and end time should not overlap with any current schedules')
                return redirect(url_for("room", id=room_id))
            
        user_house.getRoom(room_id).addToSchedule(str(startTime),int(desiredTemp),str(endTime))
        user_house.getRoom(room_id).checkNextSchedule()
        flash ("Schedule successfully added!")
        return redirect(url_for("room", id=room_id))
    else:
        room = db.execute("""SELECT * FROM rooms WHERE room_id=?;""", (room_id,)).fetchone()
        user_house.getRoom(room_id).checkNextSchedule()
        room_temp = user_house.getRoom(room_id).getCurrentTemp()
        heater_state = user_house.getRoom(room_id).heatingRunning
        schedules = user_house.getRoom(room_id).getRoomSchedule() # get all user-provided + default schedules for that room
    return render_template("room.html", title="Room", room_id=room_id, schedules=schedules, form=form, room=room, now=now, room_temp=room_temp, heater_state=heater_state)

# Edit Room page
@app.route("/edit_room/<int:id>", methods=["GET", "POST"])
def edit_room(id):
    form = RoomForm()
    room = None
    db = get_db()
    if form.validate_on_submit():
        name = form.name.data
        
        db.execute("""UPDATE rooms SET name=? WHERE room_id=?;""", (name, id))
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

    user_house.deleteRoom(int(id))
    
    flash ("Room deleted!")
    return redirect(url_for("house"))

# Deletes Schedule
@app.route("/delete_schedule/<int:room_id>/<key>")
def delete_schedule(room_id, key):
    user_house.getRoom(room_id).roomSchedule.deleteFromSchedule(str(key))
    flash ("Schedule deleted!")
    return redirect(url_for("room", id=int(room_id)))

def runApp():
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')

if __name__ == '__main__':
    try:
        t1 = Thread(target=runApp).start()
        t2 = Thread(target=main).start()
    except Exception as e:
        print("Unexpected error:" + str(e))