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
    name TEXT PRIMARY KEY,
    current_temp INTEGER NOT NULL,
    automation BOOLEAN NOT NULL,
    temp_for_turn_on INTEGER,
    time_off TIME (0),
    time_on TIME (0)
);