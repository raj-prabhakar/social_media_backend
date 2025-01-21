from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer for public user data"""
    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = fields

class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        # Check if user exists
        user = User.objects.filter(username=attrs['username']).first()
        if not user:
            raise serializers.ValidationError({
                'username': 'No account found with this username.'
            })

        # Check password
        authenticated_user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
        
        if not authenticated_user:
            raise serializers.ValidationError({
                'password': 'Incorrect password.'
            })

        # If we get here, password is correct
        attrs['user'] = authenticated_user
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token