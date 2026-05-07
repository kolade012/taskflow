from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for reading task details."""

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "celery_task_id",
            "result",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "celery_task_id",
            "result",
            "error_message",
            "created_at",
            "updated_at",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new task."""

    class Meta:
        model = Task
        fields = ["title", "description"]