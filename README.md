# Blog System

This is a simple Python blog system using **SQLAlchemy 1.4** and MySQL.  
The project demonstrates a backend system with users and posts.

## Features

- User management (username, password, role, ban status)
- Blog posts (title, content, author, published status, creation date)
- Database interactions via SQLAlchemy ORM
- Passwords and other sensitive info stored in `.env` (not in the repository)

## Requirements

- Python 3.x
- MySQL database
- Python packages (see `requirements.txt`)

```bash
python3 -m pip install -r requirements.txt