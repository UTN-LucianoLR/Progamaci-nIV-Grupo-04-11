import datetime

from core.models import Project, Task

URL_TAREAS = "/api/tasks/"  # cambiar si en core/url.py la ruta tiene otro nombre


# 1) Sin autenticar -> 401
def test_listar_tareas_sin_autenticar_devuelve_401(cliente):
    response = cliente.get(URL_TAREAS)

    assert response.status_code == 401


# 2) Aislamiento entre proyectos: ana no ve tareas de un proyecto ajeno
def test_usuario_no_ve_tareas_de_proyectos_ajenos(cliente, ana, proyecto):
    tarea_propia = Task.objects.create(project=proyecto, title="Tarea de mi proyecto")

    otro_proyecto = Project.objects.create(name="Proyecto ajeno")  # ana NO es miembro
    tarea_ajena = Task.objects.create(project=otro_proyecto, title="Tarea ajena")

    cliente.force_authenticate(user=ana)
    response = cliente.get(URL_TAREAS)

    assert response.status_code == 200
    ids = [t["id"] for t in response.data["results"]]  # "results" por la paginación
    assert tarea_propia.id in ids
    assert tarea_ajena.id not in ids


# 3) Admin del proyecto puede crear -> 201
def test_admin_puede_crear_tarea(cliente, ana, proyecto):
    cliente.force_authenticate(user=ana)
    datos = {
        "project": proyecto.id,
        "title": "Nueva tarea del admin",
        "due_date": str(datetime.date(2026, 12, 1)),
    }

    response = cliente.post(URL_TAREAS, datos, format="json")

    assert response.status_code == 201
    assert Task.objects.filter(title="Nueva tarea del admin").exists()


# 4) Miembro (no admin) no puede crear -> 403
def test_miembro_no_puede_crear_tarea(cliente, beto, proyecto):
    cliente.force_authenticate(user=beto)
    datos = {
        "project": proyecto.id,
        "title": "Tarea que no debería crearse",
        "due_date": str(datetime.date(2026, 12, 1)),
    }

    response = cliente.post(URL_TAREAS, datos, format="json")

    assert response.status_code == 403
    assert Task.objects.count() == 0  # confirmamos que NO se guardó nada