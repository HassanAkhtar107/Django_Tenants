from rest_framework import serializers
from .models import Campus, Department

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'dep_name', 'campus_id')

class CampusSerializer(serializers.ModelSerializer):
    departments = CampusSerializer(many=True, read_only=True)
    class Meta:
        model = Campus
        fields = ('id', 'campus_name', 'campus_address', 'departments')