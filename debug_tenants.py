import os
import django

# Setup django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from user.models import Client, Domain

def debug_tenants():
    print("--- Clients ---")
    for client in Client.objects.all():
        print(f"Schema: {client.schema_name}, Name: {client.name}")

    print("\n--- Domains ---")
    for domain in Domain.objects.all():
        print(f"Domain: {domain.domain}, Tenant: {domain.tenant.schema_name}, Primary: {domain.is_primary}")

if __name__ == "__main__":
    debug_tenants()
