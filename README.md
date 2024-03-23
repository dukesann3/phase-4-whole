# Assignment Tracker Employee/Project/Assignment Database

Assignment Tracker is a database for "tracking assignments" (Doh!)
It has the capabilities of accessing assignments assigned to an employee and assignments for a project.
In short, this app acts as an assignment database.

## Installing Packages

For installing python files (server files), head over to the server directory...
Assuming you are in the directory "phase-4-flatiron/phase-4-project"...
Please run this command:
```bash
cd ./server
```
to get to the server directory.


Before installing Assignment Tracker, make sure you are in a virtual environment...
Please run this command:
```bash
pipenv shell
```

Once in a virtual environment...
Please run this command:
```bash
pipenv install 
```
to install all packages in the Pipfile.

Now for installing js packages for the client side (Web Interface), head over to the client directory...
Assuming you are in the server directory...
Please run this command:
```bash
cd ../client
```
to get to the client directory.

Once in client directory...
Please run this command:
```bash
npm install
```
to install all packages in the package.json file.

## How to Start App

In order to run the app, we will first need a server and an front-end.

Assuming you are in the directory, "phase-4-flatiron/phase-4-project/server"...
Please run this command:
```bash
pipenv shell
```
to get to the virtual environment.

From there, you will need to set up the flask application and ports.
In order to do so...
Please run this command:
```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555  
```

Then, to run the server...
Please run this command:
```bash
flask --app app.py --debug run
```
Note, the debug is there to restart the server everytime a change is made to the server/backend code.

Now for setting up the client, head over to the client directory, and...
Please run this command:
```bash
npm install
```
to start the React app.

## Usage

To seed employee, project, and assignment data, head over to the server directory, then...
Please run this command:
```bash
python seed.py
```
This will seed the database with randomized parameters.
Feel free to edit them yourselves.

Once in the React App, there will be functionalities to:
1. View/Search Employees
2. Add Employees
3. Add Assignment to an Employee
4. Edit Assignment assigned to an Employee
5. Delete Assignment assigned to an Employee
6. Edit the Status of the Assignment assigned to an Employee
7. Add Projects
8. Edit Projects
9. Delete Projects
10. Add Assignment to a Project
11. Edit Assignment that is part of a Project
12. Delete Assignment that is part of a Project
13. Edit the Status of the Assignment that is part of a Project








