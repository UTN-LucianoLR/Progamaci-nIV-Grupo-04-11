import datetime

import pytest
from rest_framework.exceptions import ValidationError

from core.models import Task
from core.services import HolidayService, TaskService


# ---------- TaskService.mark_completed ----------

def test_mark_completed_con_fecha_limite_completa_la_tarea(proyecto):
    tarea = Task.objects.create(
        project=proyecto,
        title="Tarea con fecha",
        due_date=datetime.date(2026, 12, 1),
    )

    TaskService.mark_completed(tarea)

    tarea.refresh_from_db()  # releer desde la base de datos para confirmar que se guardó
    assert tarea.status == "completada"


def test_mark_completed_sin_fecha_limite_lanza_validation_error(proyecto):
    tarea = Task.objects.create(
        project=proyecto,
        title="Tarea sin fecha",
        due_date=None,
    )

    with pytest.raises(ValidationError):
        TaskService.mark_completed(tarea)

    tarea.refresh_from_db()
    assert tarea.status == "pendiente"  # no debe haber cambiado


# ---------- HolidayService.is_holiday ----------

def test_is_holiday_detecta_feriado_y_dia_normal():
    # El conftest reemplaza la API: los feriados falsos son el 1/1 y el 25/12
    assert HolidayService.is_holiday(datetime.date(2026, 12, 25)) is True
    assert HolidayService.is_holiday(datetime.date(2026, 3, 10)) is False