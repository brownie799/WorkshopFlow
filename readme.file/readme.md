# WorkshopFlow

WorkshopFlow is a smart two-wheeler workshop management
website built using FastAPI, SQLite, HTML, CSS and JavaScript.

## Features

- Separate Admin and Customer login
- Digital job card creation
- Complaint classification
- Estimated service completion time
- Job status management
- Customer vehicle tracking
- Dashboard overview

## Technology Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- FastAPI
- SQLAlchemy

Database:
- SQLite

## Installation

Create a virtual environment:

python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Install dependencies:

pip install -r backend/requirements.txt

## Start Backend

cd backend

uvicorn main:app --reload

## Start Frontend

Open another terminal:

cd frontend

python -m http.server 5500

Open:

http://127.0.0.1:5500

API Documentation:

http://127.0.0.1:8000/docs