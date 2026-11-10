
from django.db import models
from django.conf import settings
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
    ]

    STATUS_CHOICES = [
        ("pendiente", "Pendiente"),
        ("en_progreso", "En progreso"),
        ("completada", "Completada"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="media"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="pendiente"
    )
    due_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project.name})"


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("member", "Miembro"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="member"
    )

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} - {self.project} ({self.role})"


class SecurityLog(models.Model):
    action = models.CharField(max_length=100)
    detail = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} - {self.created_at}"
