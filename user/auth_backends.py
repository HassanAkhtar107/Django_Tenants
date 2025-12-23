from django.contrib.auth.backends import ModelBackend
from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

class TenantAwareAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            if email:
                user = User.objects.get(email=email)
            elif username:
                user = User.objects.get(email=username)
            else:
                None
        except User.DoesNotExist:
            return None
        
        if connection.schema_name == 'public':
            if not user.is_staff and not user.is_superuser:
                return None

        if user.check_password(password):
            return user
        return None
