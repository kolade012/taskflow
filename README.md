# TaskFlow API

A production-grade Django REST API with asynchronous background task processing using Celery and Redis.

## Tech Stack

- **Python 3.12** / **Django 6** / **Django REST Framework**
- **Celery 5.6** — distributed task queue with retry logic
- **Redis** — message broker and result backend
- **PostgreSQL** — production database
- **pytest** — full test suite with 100% pass rate
- **Black, Flake8, Isort** — code quality enforcement

## Features

- Submit tasks via REST API — processed asynchronously by Celery workers
- Real-time task status tracking (PENDING → STARTED → SUCCESS/FAILURE)
- Fault-tolerant task processing with exponential backoff retries
- UUID-based task identification
- Full test coverage with mocked Celery tasks
- System health check endpoint

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | System health check |
| POST | `/api/tasks/` | Submit a new task |
| GET | `/api/tasks/` | List all tasks |
| GET | `/api/tasks/{id}/` | Get task status and result |

## Task Lifecycle
