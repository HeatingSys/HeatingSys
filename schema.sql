DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    username TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS rooms;

CREATE TABLE rooms
(
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT,
    automation BOOLEAN NOT NULL
);

DROP TABLE IF EXISTS schedules;

CREATE TABLE schedules
(
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    room_id INTEGER NOT NULL,
    desired_temp INTEGER,
    start_time TIME (0),
    end_time TIME (0)
);