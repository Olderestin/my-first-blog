from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username':'The username should only contain alphanumeric characters'}
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs={
            'first_name': {'required': False},
            'last_name': {'required': False},

        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = {'token'}

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed('invalid credetials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Verify your email')
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': attrs.get('tokens')
        }
    
        