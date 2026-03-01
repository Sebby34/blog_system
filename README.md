# Blog System

This is a simple Python blog system using **SQLAlchemy 1.4** and MySQL.  
The project demonstrates a backend system with users and posts.

## Features

- User management (username, password, role, ban status)
- Blog posts (title, content, author, published status, creation date)
- Database interactions via SQLAlchemy ORM
- Passwords and other sensitive info stored in `.env` (not included in the repository)

## Requirements

- Python 3.x
- MySQL database
- Python packages (see `requirements.txt`)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create the MySQL Database

Make sure MySQL is running, then create a database:

```sql
CREATE DATABASE blog_system;
```

### 3. Set up environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and replace:

```
DB_PASSWORD=your_mysql_password_here
```

with your actual MySQL password.

### 4. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python3 main.py
```

The database tables will be automatically created if they do not already exist.