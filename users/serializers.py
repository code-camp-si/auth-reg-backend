from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Model Serializer for User.
    """

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False,
        )
        return user
    
    def validate_email(self, value):
        """
        Check if an account with the email already exists.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def is_valid(self, raise_exception=False):
        """
        Overridden is_valid method which includes email validation.
        """
        valid = super().is_valid(raise_exception=raise_exception)
        
        if self.initial_data.get('email'):
            try:
                self.validate_email(self.initial_data['email'])
            except serializers.ValidationError as e:
                self._errors['email'] = e.detail

        return valid



    
