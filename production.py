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

    # List of domains to create/update
    # We add both localhost (for your computer) and the Railway domain
    domains = [
        'localhost',
        '127.0.0.1',
        os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'djangotenants-production.up.railway.app')
    ]

    for domain_name in domains:
        domain, created = Domain.objects.get_or_create(
            domain=domain_name,
            tenant=tenant,
            is_primary=(domain_name == domains[-1]) # Make Railway domain the primary
        )
        if created:
            print(f"Domain '{domain_name}' created for public tenant.")
        else:
            print(f"Domain '{domain_name}' already exists.")

if __name__ == "__main__":
    create_public_tenant()
