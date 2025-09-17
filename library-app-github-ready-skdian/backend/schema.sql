
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS students;
CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE students(id INTEGER PRIMARY KEY, name TEXT, roll_no TEXT, course TEXT, email TEXT, phone TEXT);
INSERT INTO users(username,password) VALUES('SKDian Librarian Student','Password1825');
