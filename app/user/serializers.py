"""
Serializers for the user API view.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


# Serializer is a way for converting python objects or models into byte format (i.e. json file)
# Deserialization is a way for converting byte format (i.e. json) into Python objects or models

# Serializer in django, apart from the conversion, is responsible for input validation
# serializers.Serializer is base class for serialization of python objects

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    # ModelSerializer provides a data validation for the model.
    # Meta is a configuratoin class
    class Meta:
        model = get_user_model() # pass model class
        fields = ['email', 'password', 'name'] # what fields can be set by the user from request
        # we do not allow for setting is_staff field for example by using user api.

        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} # provide extra metadata for the fields.
        # we add metadata for password field - we disallow for reading the password, and setting min_length = 5

        # By default, ValidationError is raised if serializer validation fails. Then API returns 400 bad request

    # override the behavior of creating object by serializer.
    # default behavior of model serializer is passing plain text password
    # So, for user, we provide custom method for creation user, which is passing password hash during user creation

    # This method is called only if data validation passed.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # get_user_model() -> User
        # User.objects -> UserManager() # refer to User model class
        return get_user_model().objects.create_user(**validated_data)

    # Override update method for password hashing
    def update(self, instance, validated_data):
        """Update and return user."""
        # remove password from dictionary. password can be optional (i.e. user can update only email) - then it's None
        password = validated_data.pop('password', None)
        # update the rest of validated data
        user = super().update(instance, validated_data)

        # update additionally the password if entered
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        # only for browsable api (swagger) for testing & development - to make input html type password
        style={'input_type': 'password'},
        # by default django trims white characters at the end. Not expected for password.
        trim_whitespace=False,
    )

    # this method is called by the view during validation stage
    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        # serializer expects the context field should contain the request object
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
