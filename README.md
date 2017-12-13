# fake_bank
Fake bank web application for UAF CS492 Computer Security I. 


# To start
clone the repositor and navigate to fake_bank.

`cd fake_bank/`

You will need to have a MySQL database running named MuhBank.

`mysql -u root -p`
`CREATE DATABASE MuhBank;`
`exit`

Run the schema.sql file into mysql, creating the tables for you.

`mysql -u root -p MuhBank < schema.sql`

To run
`./startup.sh`

