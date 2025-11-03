from rest_framework import serializers
from . models import UsersTable

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsersTable
        fields='__all__'