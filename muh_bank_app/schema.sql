/*
Jacob McKenna
UAF CS492 Computer Security I
MySQL Bank Database
*/

-- Create Database if it doesn't exist.
CREATE Database IF NOT EXISTS MuhBank;

-- Create table if it doesn't exist.
-- User must belong to a bank.
CREATE TABLE IF NOT EXISTS User (

	id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	fname VARCHAR(40) NOT NULL,
	lname VARCHAR(40) NOT NULL,
	ssn VARCHAR(11) NOT NULL,
	email VARCHAR(100) NOT NULL,
	password VARCHAR(100) NOT NULL,
	mothersMaidenName VARCHAR(40)

) AUTO_INCREMENT = 100000000;

-- Create table if it doesn't exist.
-- User may have multiple accounts.
CREATE TABLE IF NOT EXISTS Accounts (
	
	id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	savingBalance INTEGER NOT NULL DEFAULT 100,
	checkingBalance INTEGER NOT NULL DEFAULT 0,
	owner INTEGER NOT NULL,
	password VARCHAR(100) NOT NULL,
	pin CHAR(4) NOT NULL,

	FOREIGN KEY (owner) REFERENCES User(id)

) AUTO_INCREMENT = 4000000;



SELECT fname, lname, ssn, email, User.id AS user_id, Accounts.id AS acc_id, savingBalance, checkingBalance FROM User INNER JOIN Accounts ON User.id = Accounts.owner;