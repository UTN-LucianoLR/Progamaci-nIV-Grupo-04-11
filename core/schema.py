
import graphene
from graphene_django import DjangoObjectType

from .models import Project, Task, Tag
from .services import MembershipService, NotificationService
from .serializers import TaskSerializer


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")
        convert_choices_to_enum = False


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "tags",
            "created_at",
        )
        convert_choices_to_enum = False


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "created_at")
        convert_choices_to_enum = False


# Devuelve solamente las tareas de proyectos donde el usuario es miembro.
def tasks_visible_for(user):
    if not user.is_authenticated:
        return Task.objects.none()

    return Task.objects.filter(
        project__memberships__user=user
    ).distinct()


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    task = graphene.Field(TaskType, id=graphene.ID(required=True))
    tasks_by_status = graphene.List(
        TaskType,
        status=graphene.String(required=True)
    )

    def resolve_all_projects(root, info):
        return MembershipService.projects_for(info.context.user).prefetch_related("tasks")

    def resolve_task(root, info, id):
        return tasks_visible_for(info.context.user).filter(pk=id).first()

    def resolve_tasks_by_status(root, info, status):
        return tasks_visible_for(info.context.user).filter(status=status)


class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        priority = graphene.String()
        status = graphene.String()
        due_date = graphene.Date()

    task = graphene.Field(TaskType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, project_id, title,
               description="", priority="media",
               status="pendiente", due_date=None):

        user = info.context.user

        if not user.is_authenticated:
            return CreateTask(errors=["Debés iniciar sesión."])

        project = Project.objects.filter(pk=project_id).first()

        if project is None:
            return CreateTask(errors=["El proyecto no existe."])

        if not MembershipService.is_admin(user, project):
            return CreateTask(
                errors=["Solo un administrador puede crear tareas en este proyecto."]
            )

        data = {
            "project": project_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
            "due_date": due_date,
        }

        serializer = TaskSerializer(data=data)

        if not serializer.is_valid():
            errors = [
                f"{field}: {', '.join(str(error) for error in messages)}"
                for field, messages in serializer.errors.items()
            ]
            return CreateTask(errors=errors)

        task = serializer.save()
        NotificationService.notify_task_created(task)

        return CreateTask(task=task, errors=[])


class UpdateTaskStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.String(required=True)

    task = graphene.Field(TaskType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, id, status):
        user = info.context.user

        if not user.is_authenticated:
            return UpdateTaskStatus(errors=["Debés iniciar sesión."])

        task = tasks_visible_for(user).filter(pk=id).first()

        if task is None:
            return UpdateTaskStatus(
                errors=["La tarea no existe o no tenés acceso a ella."]
            )

        if not MembershipService.is_admin(user, task.project):
            return UpdateTaskStatus(
                errors=["Solo un administrador puede modificar esta tarea."]
            )

        serializer = TaskSerializer(
            task,
            data={"status": status},
            partial=True
        )

        if not serializer.is_valid():
            errors = [
                f"{field}: {', '.join(str(error) for error in messages)}"
                for field, messages in serializer.errors.items()
            ]
            return UpdateTaskStatus(errors=errors)

        task = serializer.save()

        return UpdateTaskStatus(task=task, errors=[])


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task_status = UpdateTaskStatus.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
