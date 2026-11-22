# ToDoApp

A Django REST Framework API for managing personal to-do tasks. Users must authenticate, and can only view, change, or delete their own tasks.

## Features

- Create, list, retrieve, update, and delete tasks.
- Basic Authentication for API requests.
- Per-user task ownership.
- Task statuses: `pending`, `in_progress`, and `completed`.
- SQLite database for local development.

## Requirements

- Python
- Django
- Django REST Framework
- pytest and pytest-django (for running tests)

## Setup

From the project directory, create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages and apply database migrations:

```powershell
python -m pip install django djangorestframework pytest pytest-django
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`. Create a user with `python manage.py createsuperuser` or through the Django admin before making authenticated API requests.

## API

The API uses HTTP Basic Authentication. Send a valid username and password with each request. The task owner is set from the authenticated user; clients cannot create or access tasks on behalf of another user.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/todos/` | List the authenticated user's tasks |
| `POST` | `/api/v1/todos/` | Create a task |
| `GET` | `/api/v1/todos/{id}/` | Retrieve one of the user's tasks |
| `PUT` | `/api/v1/todos/{id}/` | Replace task fields |
| `PATCH` | `/api/v1/todos/{id}/` | Partially update a task |
| `DELETE` | `/api/v1/todos/{id}/` | Delete a task |

Example create request body:

```json
{
  "title": "Learn Django REST Framework",
  "description": "Build a task API",
  "status": "pending"
}
```

`title` must not be blank. `description` can be omitted when creating a task. A `PUT` request requires `title`, `description`, and `status`; `PATCH` accepts only the fields being changed. A task not owned by the authenticated user is returned as `404 Not Found`.

The older `/todo/tasks/` and `/todo/tasks/{id}/` paths are also available.

## Tests

Run the task test suite from the project directory:

```powershell
python -m pytest task\tests -v
```

Pytest is configured in [pytest.ini](pytest.ini). API tests are in [task/tests/test_views.py](task/tests/test_views.py), with shared fixtures in [task/tests/conftest.py](task/tests/conftest.py). Pytest-django creates an isolated test database for database-backed tests.
