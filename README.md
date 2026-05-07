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

## Local Setup

### Prerequisites
- Python 3.10+
- Redis running on localhost:6379
- PostgreSQL (optional — SQLite used by default)

### Installation

```bash
git clone https://github.com/kolade012/taskflow.git
cd taskflow
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate
pip install -r requirements.txt
python manage.py migrate
```

### Running the API

```bash
# Terminal 1 — Django server
python manage.py runserver

# Terminal 2 — Celery worker
celery -A core worker --loglevel=info -P solo

# Terminal 3 — Test the API
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Processing something"}'
```

### Running Tests

```bash
pytest tasks/tests.py -v
```

## Task Lifecycle