import requests

from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Task, Project, ProjectMembership
from .repositories import TaskRepository


class TaskService:
    @staticmethod
    def mark_completed(task: Task) -> Task:
        # Misma regla de negocio que TaskSerializer.validate (Clase 4)
        if not task.due_date:
            raise ValidationError(
                "No se puede marcar una tarea como completada sin fecha límite registrada."
            )
        task.status = "completada"
        task.save(update_fields=["status"])
        return task

    @staticmethod
    def tasks_overdue(queryset=None):
        if queryset is None:
            queryset = TaskRepository.get_queryset()
        today = timezone.now().date()
        return queryset.filter(due_date__lt=today).exclude(status="completada")


class HolidayService:
    API_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    COUNTRY_CODE = "US"
    TIMEOUT = 5  # segundos máximos de espera a la API

    @classmethod
    def get_holidays(cls, year: int) -> list[str]:
        cache_key = f"holidays_{year}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        try:
            url = cls.API_URL.format(year=year, country_code=cls.COUNTRY_CODE)
            response = requests.get(url, timeout=cls.TIMEOUT)
            response.raise_for_status()
            dates = [item["date"] for item in response.json()]
            cache.set(cache_key, dates, timeout=60 * 60 * 24)
        except (requests.RequestException, KeyError, ValueError):
            dates = []
            cache.set(cache_key, dates, timeout=60 * 5)
        return dates

    @classmethod
    def is_holiday(cls, some_date) -> bool:
        return str(some_date) in cls.get_holidays(some_date.year)


class MembershipService:

    @staticmethod
    def projects_for(user):
        if not user.is_authenticated:
            return Project.objects.none()

        return Project.objects.filter(
            memberships__user=user
        ).distinct()

    @staticmethod
    def is_member(user, project):
        if not user.is_authenticated:
            return False

        return ProjectMembership.objects.filter(
            user=user,
            project=project
        ).exists()

    @staticmethod
    def is_admin(user, project):
        if not user.is_authenticated:
            return False

        return ProjectMembership.objects.filter(
            user=user,
            project=project,
            role="admin"
        ).exists()


class NotificationService:

    @staticmethod
    def notify_task_created(task):
        subject = f"Nueva tarea: {task.title}"
        message = (
            f"Se creó una nueva tarea en el proyecto {task.project.name}."
        )

        members = ProjectMembership.objects.filter(
            project=task.project
        ).select_related("user")

        for membership in members:
            NotificationService._send(
                subject,
                message,
                membership.user.email
            )

    @staticmethod
    def _send(subject, message, recipient):
        if not recipient:
            return

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=True
        )