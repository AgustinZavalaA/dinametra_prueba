# Dinametra test

FastAPI TODO application for managing tasks and automated cleanup of completed tasks.

## Author

- **Name**: Agustin Zavala Arias
- **Start Time**: ~ Jan 06 23:31
- **End Time**: ~ Jan 07 02:50

# Tech and Libraries Used

- Python: I used python as it is the language I am most invested on (data analysis and robotics).
- FastAPI: Really good for making REST apps in python, provides great
integration with python and other libraries.
- Uvicorn: ASGI server makes running the app with live reload so it
helps a ton in debugging/building the app.
- SqlAlchemy: Database ORM that helps in managing the database in a descriptive way.
- SQLITE: Lightweight and easy to configure database.

# Instalation

## Verify Python Instalation

Make sure to have python 3.12 installed, to verify it Run
`python --version # should display 3.12`

If python is not installed follow the [Python Installation Guide](https://www.python.org/downloads/)

## Clone repo

Run the following command in the directory you want to have the code
`git clone <https://github.com/AgustinZavalaA/dinametra_prueba.git>`

## Create virtual enviroment

It is recommended but not necesary to create a virtual enviroment,
I have tested this using the following command
`python -m venv venv`

Activate Virtual Environment with:

- For UNIX-like systems (Linux, macOS): `source venv/bin/activate`
- For Windows: `.\venv\Scripts\activate`

## Install Libraries

To install all libraries used, run the following command:
`pip install -r requirements.txt`

## Run app

To run the app with live reload, use this command:

`uvicorn main:app --reload`

# Usage

I did not had enough time to complete a UI, so you can try all endpoints in any app you like, but FastAPI provides an incredible way to check it

Make sure to have the app running.

In a browser go to <http://127.0.0.1:8000/docs>
here you can see all the implemented endpoints and try them out

Create a User to be able to view and create Tasks

After creating a User, authorize the enpoints clicking the "Authorize" button on the top left of the page

Remember that every time you run the app, the thread to delete completed Tasks run, so if you don't want to wait you can stop and run the app again to see the behavior

# Another projects that may be interesting

[Mexican Robot Tournament Code](https://github.com/AgustinZavalaA/RLP_TMR2023.git)
All the code used to run the robot in the tournament,
[DataShip](https://github.com/AgustinZavalaA/DataShip.git)
Platform I did in University to perform data analysis on the web.
