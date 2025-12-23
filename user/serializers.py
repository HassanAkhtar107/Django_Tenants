from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
# from .models import User, Company, CompanyBranches, Author, Books, Values
from .models import User, Client, Domain
from django_tenants.utils import schema_context

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    schema_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role', 'schema_name')
    
    def create(self, validated_data):
        schema_name = validated_data.pop('schema_name').lower()
        tenant_name =schema_name.capitalize()
        tenant = Client.objects.create(
            schema_name=schema_name,
            name=tenant_name
        )
        Domain.objects.create(
            domain=f"{schema_name}.localhost",
            tenant=tenant,
            is_primary=True
        )
        with schema_context(schema_name):
            user = User.objects.create_user(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                password=validated_data['password'],
                role=validated_data.get('role', 'user')
            )
            return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name','role')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')

# class BranchesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyBranches
#         fields = ('id', 'company', 'branch_name', 'branch_address')

# class CompanySerializer(serializers.ModelSerializer):
#     branches = BranchesSerializer(many=True, read_only=True)
#     class Meta:
#         model = Company
#         fields = ('id', 'company_name','branches')
    
# class AutherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ('id', 'book', 'author_name')

# class BookSerializer(serializers.ModelSerializer):
#     author_books = AutherSerializer(many=True, read_only=True)
#     class Meta:
#         model = Books
#         fields = ('id', 'title', 'author','author_books')
        
# class valuesSerializer(serializers.ModelSerializer):
#     sum_val = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Values
#         fields = ('id', 'value', 'number', 'sum_val')