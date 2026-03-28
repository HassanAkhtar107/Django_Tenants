from user.models import Client, Domain
import os

# Your Railway domain (e.g. djangotenants-production.up.railway.app)
RAILWAY_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'djangotenants-production.up.railway.app')

# Create the public tenant
tenant, created = Client.objects.get_or_create(schema_name='public', name='Public Tenant')

# Create the domain for Railway
Domain.objects.get_or_create(domain=RAILWAY_DOMAIN, tenant=tenant, is_primary=True)
print(f"Public tenant and domain '{RAILWAY_DOMAIN}' created successfully.")
