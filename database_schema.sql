DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS signedInUsers;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
       email VARCHAR(200) NOT NULL,
       password VARCHAR(60) NOT NULL,
       firstName VARCHAR(200) NOT NULL,
       lastName VARCHAR(200) NOT NULL,
       gender VARCHAR(10) NOT NULL,
       city VARCHAR(200) NOT NULL,
       country VARCHAR(200) NOT NULL,
       PRIMARY KEY (email));

CREATE TABLE signedInUsers (
       token VARCHAR(36) NOT NULL,
       email VARCHAR(200) NOT NULL,
       PRIMARY KEY (token)
       FOREIGN KEY (email) REFERENCES users(email));

CREATE TABLE messages (
       messageId INT NOT NULL,
       message TEXT NOT NULL,
       datePosted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       wallEmail VARCHAR(200) NOT NULL,
       writer VARCHAR(200) NOT NULL,
       PRIMARY KEY (messageId),
       FOREIGN KEY (wallEmail) REFERENCES users(email),
       FOREIGN KEY (writer) REFERENCES users(email));

       
       