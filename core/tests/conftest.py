import pytest
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework.throttling import SimpleRateThrottle

from core.models import Project, ProjectMembership
from core.services import HolidayService


# =====================================================================
# ENTORNO AISLADO: autouse=True hace que se apliquen a TODOS los tests
# =====================================================================

@pytest.fixture(autouse=True)
def channel_layer_en_memoria(settings):
    """Usa un channel layer en memoria, así los tests no necesitan Redis."""
    settings.CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }


@pytest.fixture(autouse=True)
def feriados_falsos(monkeypatch):
    """Reemplaza la llamada a la API de feriados, así no se necesita internet."""
    def get_holidays_falso(cls, year):
        return [f"{year}-01-01", f"{year}-12-25"]

    monkeypatch.setattr(HolidayService, "get_holidays", classmethod(get_holidays_falso))


@pytest.fixture(autouse=True)
def sin_throttling(monkeypatch):
    """Desactiva los límites de pedidos (por ejemplo, 5 logins por minuto)."""
    monkeypatch.setattr(SimpleRateThrottle, "allow_request", lambda self, request, view: True)


@pytest.fixture(autouse=True)
def cache_limpia():
    """Vacía la caché antes y después de cada test, para que no se mezclen datos."""
    cache.clear()
    yield
    cache.clear()


# =====================================================================
# DATOS DE PRUEBA
# =====================================================================

@pytest.fixture
def ana(db, django_user_model):
    """Usuaria que será ADMIN del proyecto."""
    return django_user_model.objects.create_user(
        username="ana", email="ana@test.com", password="clave-segura-123"
    )


@pytest.fixture
def beto(db, django_user_model):
    """Usuario que será MIEMBRO (no admin) del proyecto."""
    return django_user_model.objects.create_user(
        username="beto", email="beto@test.com", password="clave-segura-123"
    )


@pytest.fixture
def proyecto(db, ana, beto):
    """Proyecto con ana como admin y beto como miembro."""
    p = Project.objects.create(name="Proyecto de prueba")
    ProjectMembership.objects.create(project=p, user=ana, role="admin")
    ProjectMembership.objects.create(project=p, user=beto, role="member")
    return p


@pytest.fixture
def cliente():
    """Cliente HTTP para llamar a la API. Arranca SIN autenticar."""
    return APIClient()