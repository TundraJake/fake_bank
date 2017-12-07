/*
Jacob McKenna
UAF CS492 Computer Security I
MySQL Bank Database
*/

-- Create Database if it doesn't exist.
CREATE Database IF NOT EXISTS MuhBank;

-- Create table if it doesn't exist.
CREATE TABLE IF NOT EXISTS Bank (
	
	id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	name VARCHAR(40) NOT NULL,
	balance INTEGER NOT NULL

) AUTO_INCREMENT = 12345678;

-- Create table if it doesn't exist.
-- User must belong to a bank.
CREATE TABLE IF NOT EXISTS User (

	id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	ssn VARCHAR(11) NOT NULL,
	fname VARCHAR(40) NOT NULL,
	lname VARCHAR(40) NOT NULL,
	mothersMaidenName VARCHAR(40),
	userOfBank INTEGER NOT NULL, 

	FOREIGN KEY (userOfBank) REFERENCES Bank(id)

) AUTO_INCREMENT = 100000000;

-- Create table if it doesn't exist.
-- User may have multiple accounts.
CREATE TABLE IF NOT EXISTS Accounts (
	
	id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	password VARCHAR(40) NOT NULL,
	pin CHAR(4) NOT NULL,
	balance INTEGER NOT NULL,
	owner INTEGER NOT NULL,

	FOREIGN KEY (owner) REFERENCES User(id)

) AUTO_INCREMENT = 4000000;
