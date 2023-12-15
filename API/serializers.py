from rest_framework import serializers
from users.models import CustomUser
from blog.models import Post, Comment, PostImage
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone



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
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = {'password', 'uidb64', 'token'}

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            user.set_password(password)
            user.save()
            
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validate_data):
        author = self.context['request'].user
        
        comment = Comment.objects.create(author=author, **validate_data)
        return comment

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def validate(self, attrs):
        super().validate(attrs)

        post = attrs.get('post')
        if post.images.count() >= 4:
            raise serializers.ValidationError({'error': 'Post has maximum number of PostImages'})
        
        if post.author != self.context['request'].user:
            raise serializers.ValidationError({'error': 'Not the author of this post'})
        return attrs

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    published_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'published_date', 'title', 'text', 'images', 'comments']

    def create(self, validate_data):
        author = self.context['request'].user
        
        post = Post.objects.create(author=author, published_date=timezone.now(), **validate_data)
        return post
    
class UserProfileSerializer(serializers.ModelSerializer):
    post_set = PostSerializer(many=True, read_only=True)
    username = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'status', 'description', 'user_image', 'post_set']