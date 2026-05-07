import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=5,
    name="tasks.process_task",
)
def process_task(self, task_id: str) -> dict:
    """
    Process a submitted task asynchronously.
    Retries up to 3 times on failure with 5 second delay.
    """
    from .models import Task

    try:
        task = Task.objects.get(id=task_id)
        task.status = Task.Status.STARTED
        task.celery_task_id = self.request.id
        task.save(update_fields=["status", "celery_task_id", "updated_at"])

        logger.info(f"Processing task {task_id}: {task.title}")

        # Simulate real processing work
        result = f"Task '{task.title}' completed successfully at {timezone.now()}"

        task.status = Task.Status.SUCCESS
        task.result = result
        task.save(update_fields=["status", "result", "updated_at"])

        logger.info(f"Task {task_id} completed successfully")
        return {"task_id": task_id, "status": "SUCCESS", "result": result}

    except Task.DoesNotExist:
        logger.error(f"Task {task_id} not found")
        raise

    except Exception as exc:
        logger.error(f"Task {task_id} failed: {exc}")

        try:
            task.status = Task.Status.RETRYING
            task.error_message = str(exc)
            task.save(update_fields=["status", "error_message", "updated_at"])
        except Exception:
            pass

        raise self.retry(
            exc=exc,
            countdown=2 ** self.request.retries,
        )


@shared_task(name="tasks.health_check")
def health_check() -> dict:
    """Periodic health check task run by Celery Beat."""
    logger.info("Health check executed")
    return {"status": "healthy", "timestamp": str(timezone.now())}