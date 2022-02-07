from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

# The ModelSerializer performs validation FOR you and you can access the data using 'validated_data'
# If you want to drop down to using Serializer classes instead, then you need to define the validation rules explicitly
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        # Instead of referring to User directly, you should reference the user model using django.contrib.auth.get_user_model().
        # This method will return the currently active user model – the custom user model if one is specified, or User otherwise.
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encripted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correcly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
