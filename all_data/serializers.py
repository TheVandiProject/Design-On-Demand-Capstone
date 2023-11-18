from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    email_address = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = Users
        fields = ('id', 'email_address', 'username', 'password')
