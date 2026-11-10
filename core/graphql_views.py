from django.http import JsonResponse
from graphene_django.views import GraphQLView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        authentication = JWTAuthentication()

        try:
            result = authentication.authenticate(request)
        except AuthenticationFailed as error:
            return JsonResponse({"detail": str(error)}, status=401)

        if result is not None:
            request.user, request.auth = result

        return super().dispatch(request, *args, **kwargs)