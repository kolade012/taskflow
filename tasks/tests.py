import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_task():
    return Task.objects.create(
        title="Test Task",
        description="A test task description",
    )


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_check_returns_200(self, api_client):
        url = reverse("health-check")
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["status"] == "healthy"
        assert response.data["service"] == "TaskFlow API"


@pytest.mark.django_db
class TestTaskCreation:
    @patch("tasks.views.process_task.delay")
    def test_create_task_success(self, mock_delay, api_client):
        url = reverse("task-list-create")
        payload = {
            "title": "My Background Task",
            "description": "Processing something important",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "My Background Task"
        assert response.data["status"] == "PENDING"
        mock_delay.assert_called_once()

    @patch("tasks.views.process_task.delay")
    def test_create_task_missing_title(self, mock_delay, api_client):
        url = reverse("task-list-create")
        payload = {"description": "No title provided"}
        response = api_client.post(url, payload, format="json")
        assert response.status_code == 400
        mock_delay.assert_not_called()


@pytest.mark.django_db
class TestTaskRetrieval:
    def test_list_tasks(self, api_client, sample_task):
        url = reverse("task-list-create")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_get_task_detail(self, api_client, sample_task):
        url = reverse("task-detail", kwargs={"pk": sample_task.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert str(response.data["id"]) == str(sample_task.id)
        assert response.data["title"] == "Test Task"

    def test_get_nonexistent_task(self, api_client):
        import uuid
        url = reverse("task-detail", kwargs={"pk": uuid.uuid4()})
        response = api_client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskModel:
    def test_task_default_status_is_pending(self, sample_task):
        assert sample_task.status == Task.Status.PENDING

    def test_task_str_representation(self, sample_task):
        assert str(sample_task) == "Test Task [PENDING]"

    def test_task_has_uuid_primary_key(self, sample_task):
        import uuid
        assert isinstance(sample_task.id, uuid.UUID)