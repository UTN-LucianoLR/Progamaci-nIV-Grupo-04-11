from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from core import views
from core.graphql_views import JWTGraphQLView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.url")),
    path("graphql/", csrf_exempt(JWTGraphQLView.as_view(graphiql=True))),
]