
'''import json

i = 1
ir = 2

# Data to be written
dictionary = {
    "schedule_id": i,
    "room_id": ir,
    "desired_temp": 8.6,
    "start_time": "9976770500",
    "end_time": 8.6,
    "schedule_state": False
}
 
# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("userSchedules.json", "w") as outfile:
    outfile.write(json_object)'''

from house import House

roo = House()

r = roo.getAllRooms()
print(r)