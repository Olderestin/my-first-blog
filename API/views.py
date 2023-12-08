from django.urls import reverse
from django.conf import settings
from users.models import CustomUser
from blog.models import Post, PostImage
from .serializers import LogoutSerializer, RegisterSerializer, EmailVerificationSerializer, LoginSerializer, RequestPasswordResetSerializer, SetNewPasswordSerializer, PostSerializer, PostImageSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions, viewsets, mixins, parsers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from users.tasks import sending_email_task
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .permissions import IsOwner, ProfileIsOwner, PostImageIsOwner
from django.shortcuts import get_object_or_404


# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('api-email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        email_subject = 'Verify your email'
        sending_email_task.delay(email_subject, email_body, to=[user.email])
        return Response(user_data, status=status.HTTP_201_CREATED)
    
class VerifyEmail(views.APIView):

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config], tags=['Authentication'])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = CustomUser.objects.get(pk=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Succesfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoguotAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = RequestPasswordResetSerializer

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):

        email = request.data.get('email', '')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('api-password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relative_link
            email_body = 'Hello, \n Use link below to reset your password \n'+absurl
            email_subject = 'Reset your password'
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send()
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There is no user with this email'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(views.APIView):

    @swagger_auto_schema(tags=['Authentication'])
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
        
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials valid', 'uidb4': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response('error', 'Token is not valid, please request a new one', status=status.HTTP_401_UNAUTHORIZED)
        

class SetNewPassword(generics.GenericAPIView):
    
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(tags=['Authentication'])
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        return (permission() for permission in permission_classes)

class PostImageViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    permission_classes = (permissions.IsAuthenticated, PostImageIsOwner, )

class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

    lookup_field = 'username'

    http_method_names = ['get', 'patch']
    
    
    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, ProfileIsOwner]
        return (permission() for permission in permission_classes)
    
    def get_object(self):
        queryset = self.get_queryset()

        lookup_value = self.kwargs[self.lookup_field]

        obj = get_object_or_404(queryset, **{self.lookup_field: lookup_value})
        self.check_object_permissions(self.request, obj)
        return obj









