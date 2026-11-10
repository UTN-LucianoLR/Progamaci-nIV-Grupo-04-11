
from datetime import date

from rest_framework import serializers

from .models import Project, Task, Tag
from .services import HolidayService


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    due_on_holiday = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "tags",
            "created_at",
            "due_on_holiday",
        ]

    def validate_due_date(self, value):
        # No permite fechas pasadas nuevas o modificadas.
        if value and value < date.today():
            if self.instance is None or value != self.instance.due_date:
                raise serializers.ValidationError(
                    "La fecha límite no puede estar en el pasado."
                )
        return value

    def validate(self, data):
        # En PATCH, conserva los valores que no fueron enviados.
        def actual(campo):
            return data.get(
                campo,
                getattr(self.instance, campo, None)
            )

        status = actual("status")
        due_date = actual("due_date")
        project = actual("project")

        if status == "completada" and not due_date:
            raise serializers.ValidationError(
                "No se puede marcar una tarea como completada "
                "sin fecha límite registrada."
            )

        if status == "en_progreso" and project is not None:
            otras_completadas = project.tasks.filter(
                status="completada"
            )

            if self.instance is not None:
                otras_completadas = otras_completadas.exclude(
                    pk=self.instance.pk
                )

            if not otras_completadas.exists():
                raise serializers.ValidationError(
                    "No se puede pasar a 'en_progreso' si el proyecto "
                    "no tiene ninguna tarea completada todavía."
                )

        return data

    def get_due_on_holiday(self, obj):
        if not obj.due_date:
            return False

        return HolidayService.is_holiday(obj.due_date)


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "tasks",
            "created_at",
        ]
