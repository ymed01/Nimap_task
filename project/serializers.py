# serializers.py

from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)
    # client = ClientSerializer(read_only=True)
    client_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'users', 'created_at', 'created_by']

    def get_client_name(self, obj):
        return obj.client.client_name if obj.client else None
    

class ProjectForUserSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by']

class ProjectForUserDetailSerializer(serializers.ModelSerializer):
    """Separate serializer for ProjectForUser"""
    name = serializers.CharField(source='project_name', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name']  # Include only id and name

class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)
    projects = ProjectForUserDetailSerializer(many=True, read_only=True)  # Nested projects list

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']




class ClientDetailUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']

    def update(self, instance, validated_data):
        # Set the updated_at field to the current time (timezone aware)
        instance.updated_at = timezone.now()

        # Update the client_name field if it exists in validated_data
        instance.client_name = validated_data.get('client_name', instance.client_name)

        instance.save()
        return instance