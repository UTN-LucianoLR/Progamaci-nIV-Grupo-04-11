from datetime import date
from rest_framework import serializers
from .models import Project, Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "project", "title", "description",
            "priority", "status", "due_date", "tags", "created_at",
        ]

    def validate_due_date(self, value):
        # Solo se rechaza una fecha pasada si es nueva o si cambió; así se puede
        # editar (PUT/PATCH) una tarea vieja sin tener que tocar su fecha límite.
        if value and value < date.today():
            if self.instance is None or value != self.instance.due_date:
                raise serializers.ValidationError("La fecha límite no puede ser en el pasado.")
        return value

    def validate(self, data):
        # En un PATCH, "data" trae solo los campos enviados: para los demás
        # se usa el valor que ya tiene la instancia guardada.
        def actual(campo):
            return data.get(campo, getattr(self.instance, campo, None))

        status = actual("status")
        due_date = actual("due_date")
        project = actual("project")

        if status == "completada" and not due_date:
            raise serializers.ValidationError(
                "No se puede marcar una tarea como completada sin fecha límite registrada."
            )

        if status == "en_progreso" and project is not None:
            otras_completadas = project.tasks.filter(status="completada")
            if self.instance is not None:
                # la propia tarea no cuenta como "otra tarea completada"
                otras_completadas = otras_completadas.exclude(pk=self.instance.pk)
            if not otras_completadas.exists():
                raise serializers.ValidationError(
                    "No se puede pasar a 'en_progreso' si el proyecto no tiene "
                    "ninguna tarea completada todavía."
                )
        return data


# Serializer de Project (depende de Task)
class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "tasks", "created_at"]