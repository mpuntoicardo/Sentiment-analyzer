from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta(object):
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'password','last_login', 'date_joined']

    def validate_email(self, value):
        # Check if any user already exists with this email.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value