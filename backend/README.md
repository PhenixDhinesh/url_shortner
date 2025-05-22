# Backend Service

This directory contains the Flask API service for the URL Shortener. It handles the core logic for shortening URLs, redirecting them, and managing data persistence with PostgreSQL.

## Features

* **URL Shortening**: Generates short codes for long URLs and stores them in the database.
* **Redirection**: Redirects users from a short code to the original long URL.
* **Database Management**: Uses Flask-SQLAlchemy for ORM and Flask-Migrate for database migrations.

---

## Prerequisites

Before running the backend, ensure you have:

* **Python 3.9+** and **pip**.
* A **PostgreSQL database** instance running and accessible.

---

## Setup & Running

Follow these steps to set up and run the backend service.

### 1. Navigate to the Directory

```bash
cd my-advanced-url-shortener/backend
```

### 2. Configure Environment Variables

Create a file named `.env` in this `backend/` directory. Fill in your PostgreSQL connection details and other necessary configurations.

```plaintext
# .env file for backend service

# Flask Application Configuration
FLASK_CONFIG=development
FLASK_APP=app.py

# Database Configuration (PostgreSQL)
# IMPORTANT: Replace with your actual PostgreSQL connection details.
# Example: postgresql://user:password@host:port/database_name
DATABASE_URL=postgresql://admin:password@localhost:5432/url_shortener_db

# Application Secret Key
SECRET_KEY=your_development_secret_key

# Base URL for the Shortener (used in URL generation)
BASE_URL=http://localhost:5000
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Database Setup (First Time Only)

For the very first time you set up the database, you need to initialize Flask-Migrate and apply the initial schema.

#### a. Set Flask App Variable:

```bash
export FLASK_APP=app.py
# On Windows: set FLASK_APP=app.py
```

#### b. Initialize Migrations: (Run this command only once for the project)

```bash
flask db init
```

#### c. Create Initial Migration: (This generates the script for your url_mappings table)

```bash
flask db migrate -m "Initial database schema"
```

#### d. Apply Migrations: (This creates the tables in your PostgreSQL database)

```bash
flask db upgrade
```

### 5. Running the Application

To start the Flask development server:

```bash
flask run --host=0.0.0.0 --port=5000
```

The application will now be running and accessible at http://localhost:5000.

### 6. Managing Database Changes (When models.py changes)

If you modify your database models (`backend/models.py`) in the future, follow these steps to update your database schema:

#### a. Generate a new migration script:

```bash
flask db migrate -m "Description of your changes"
```

#### b. Apply the migration:

```bash
flask db upgrade
```

### 7. Testing

* **Health Check**: GET request to http://localhost:5000/_health
* **Shorten URL**: POST request to http://localhost:5000/api/v1/shorten with JSON body: `{"long_url": "https://your.long.url.com"}`
* **Redirect**: GET request to http://localhost:5000/YOUR_SHORT_CODE
