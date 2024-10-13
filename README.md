# Flask API Application

## Overview

This is a Flask API application that provides user authentication and management functionality. It supports JWT-based authentication and is designed to be deployed both locally and in a production environment using Docker.

## Table of Contents

- [Flask API Application](#flask-api-application)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
    - [Using a WSGI Server](#using-a-wsgi-server)
    - [Using Docker](#using-docker)
  - [E-Commerce Models ER Diagram](#e-commerce-models-er-diagram)

## Requirements

- Python 3.8 or higher
- Flask 2.0 or higher
- Flask-RESTX
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Dotenv
- Waitress (for production)

## Installation

1. **Clone the Repository:**

   Open a terminal and run the following command to clone the repository:

   ```bash
   git clone https://github.com/nooreldeensalah/Flask_API/
   cd Flask_API
   ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv .venv
    ```

3. **Activate the Virtual Environment:**

   - On Windows:

   ```bash
   .venv\Scripts\activate
   ```

   - on MacOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. **Install Dependencies:**

    Use `pip` to install the required dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Set up Environment Variables:

    Create a .env file in the root of your project with the following content:

    ```plaintext
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///app.db
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

    Make sure to replace your_secret_key and your_jwt_secret_key with your actual secret keys.

2. Run the Application:

### Using a WSGI Server

You can start the Flask application using a production-quality WSGI server (`waitress`):

```bash
waitress-serve --port=8000 main:app
```

### Using Docker

You can also run the application by building a docker image and deploying a container out of it:

```bash
# Build the Docker image
docker build -t flask-app-demo .

# Run the docker container
docker run -p 8000:8000 -e SECRET_KEY=mysecretkey123 -e SQLALCHEMY_DATABASE_URI=sqlite:///app.db -e JWT_SECRET_KEY=myjwtsecretkey456 flask-app-demo
```

The application is accessible at `http://localhost:8000`, you can access the Swagger documentation at `http://localhost:8000/docs`

## E-Commerce Models ER Diagram

An ER diagram was generated using `sqlalchemy-data-model-visualizer` from the existing SQLAlchemy models.
![ER Diagram](./diagram.svg)
