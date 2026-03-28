import os
import django

# Setup django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from user.models import Client, Domain

def create_public_tenant():
    # Create the public tenant if it doesn't exist
    tenant, created = Client.objects.get_or_create(
        schema_name='public',
        name='Public Tenant',
    )
    if created:
        print("Public tenant created.")

    # Get domain from environment or fallback
    domain_name = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'djangotenants-production.up.railway.app')
    
    # Create the domain for public tenant
    domain, created = Domain.objects.get_or_create(
        domain=domain_name,
        tenant=tenant,
        is_primary=True
    )
    if created:
        print(f"Domain '{domain_name}' created for public tenant.")
    else:
        # If it already exists but is different, update it
        if domain.domain != domain_name:
            domain.domain = domain_name
            domain.save()
            print(f"Updated domain to '{domain_name}'.")
        else:
            print(f"Domain '{domain_name}' already exists.")

if __name__ == "__main__":
    create_public_tenant()
