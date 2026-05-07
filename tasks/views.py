import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer
from .tasks import process_task

logger = logging.getLogger(__name__)


class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/tasks/ — List all tasks
    POST /api/tasks/ — Submit a new task for processing
    """
    queryset = Task.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = Task.objects.create(**serializer.validated_data)

        # Fire Celery task asynchronously
        process_task.delay(str(task.id))

        logger.info(f"Task {task.id} submitted for processing")

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(generics.RetrieveAPIView):
    """
    GET /api/tasks/{id}/ — Retrieve task status and result
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]


class HealthCheckView(APIView):
    """
    GET /api/health/ — System health check
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "healthy",
            "service": "TaskFlow API",
            "version": "1.0.0",
        })