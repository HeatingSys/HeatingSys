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
    username TEXT NOT NULL,
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    automation BOOLEAN NOT NULL
);

DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule
(
    desired_temp INTEGER,
    time_off TIME (0),
    time_on TIME (0)
);