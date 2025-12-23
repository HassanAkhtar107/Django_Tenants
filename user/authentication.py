from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import connection
from rest_framework.exceptions import AuthenticationFailed

class TenantJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth = super().authenticate(request)
        if not auth:
            return None

        user, token = auth

        token_tenant = token.get('tenant')
        current_tenant = connection.schema_name

        if token_tenant != current_tenant:
            raise AuthenticationFailed("Token not valid for this tenant")

        return user, token
