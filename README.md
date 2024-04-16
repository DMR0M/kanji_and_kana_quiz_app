# Kanji and Kana Quiz Web Application
This is a website for practicing your hiragana, katakana, and kanji vocabulary

## Setup
### 1: Download Dependencies

Create a python virtual environment (make sure you have Python 3.9 and up installed)

```bash
python -m venv .venv
```

Activate the python virtual environment created

For Windows:

```bash
source .venv/Scripts/activate
```

For Mac OS:

```bash
source .venv/bin/activate
```

Use the package manager pip to install all required dependencies using the requirements.txt file

```bash
pip install -r requirements.txt
```

### 2: Configuring the database

The website connects to a PostgreSQL database, make sure you have Postgres installed (preferrably pgAdmin also)
Create a PostgreSQL database named "KanjiQuiz" in Postgres

See web_app_core/web_app_core/.env file
```
DB_NAME=KanjiQuiz
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=23400
```
Configure all properties to match your database credentials

### 3: Creating Database Migrations

Once the postgresql database is configured, we can now connect to it and create the required tables in Django

Go to the directory where manage.py file is located

```bash
cd web_app_core
```

Run to create migration files

```bash
python manage.py makemigrations
```

Then run

```bash
python manage.py migrate
```

To create the tables in your database

### 4: Importing Data

When all the tables have been created, you can now import the data to the Kanji Definition Table

Run the following SQL script in pgAdmin scripts/Kanji_Definitions_Data.sql


### 5: Open The Website

Go to the directory where manage.py file is located

Run to run the server
```bash
python manage.py runserver
```
