# Task Tracker Backend application

## <span style='color:red'>Description</span>

This is a simplified version of a team task tracker backend, inspired by tools like Trello or Jira, built with FastAPI. 

## Authentication
The project includes user authentication via JWT tokens, supports login using a username and password, enhancing security and access control.
## Role System

The system implements two roles: ADMIN and USER.

### ADMIN
- Has full control and can create, edit, and delete tasks without restrictions.
- Only ADMINs can edit user accounts.

### USER
- Can create tasks and become the responsible person for them.
- Can add themselves and other users as assignees.
- Can edit tasks only if they are either the responsible person or an assignee.
- Upon registration, users are set to `is_active = false`, meaning they do not have access to the application until activated by an ADMIN.

### Additional Permissions
- **Priority, Responsible Person** : Can be changed by either ADMIN or the responsible person.
- **Deletion**: Only ADMINs can delete tasks.

## Email Notifications
The project includes a mock email sending feature that logs sent emails to a file named `email_log.txt`.

## To start the application using Docker:

### After the containers are running, Alembic migrations will be executed automatically, and a superuser will be created only if there are no other users in the database.
```bash
# Preferred

# clone repository
git clone <repository_url>

# You should be at the root of the project
cd <repository_directory>

# Build docker image from Dockerfile
- docker build .

# Run containers database and application
- docker compose up 
_________________________________________

## Manual second Way

# Build image
docker compose build --no-cache

# Run containers
docker compose up -d

# Access the application container
docker exec -it tasks_app bash

# Run migration
alembic upgrade head

# Initialize superuser
python src/initial_data.py
```

### <span style='color:yellow'>Accessing the Application</span>

The application will be available at http://127.0.0.1:8000.
You can also access the interactive API documentation at http://127.0.0.1:8000/docs

## Development environment
### <span style='color:yellow'>Instal Deps</span>
```bash
# install pipenv
pip install pipenv

# activate virtual env
pipenv shell

# install deps
pipenv sync --dev
```
## Usage code quality tools
```bash
# The pre-commit hook will be automatically run
- flake8, black, isort
```

