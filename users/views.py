import jwt
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_yasg.utils import swagger_auto_schema
from .utils import (
    get_headers, 
    get_login_request_body,
    get_create_account_request_body,
    get_forgot_password_request_body,
    get_reset_password_request_body
)


@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_login_request_body()
)
@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({ 'message': 'Invalid credentials' }, status=status.HTTP_401_UNAUTHORIZED)
        
        if check_password(password, user.password):
            token_payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
            user_data = { 'user_id': user.id, 'username': username, 'email': user.email }
            return Response({ 'token': token, 'user': user_data }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        return Response({'message': 'Something went wrong !'}, status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_create_account_request_body()
)
@api_view(['POST'])
def create_account(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            hashed_password = make_password(request.data.get('password'))
            serializer.save(password=hashed_password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        return Response({'message': 'Something went wrong !'}, status=status.HTTP_400_BAD_REQUEST)
    


@swagger_auto_schema(
    method='get',
    manual_parameters=get_headers()
)
@api_view(['GET'])
def check_auth(request):
    """
    API endpoint to check token.

    Parameters (headers):
        - token
    Returns:
        - 200: OK.
        - 400 Bad Request: Some error occured.
    """
    try:
        user = User.objects.get(id=request.jwt_payload['user_id'])
        print('user: ', user)

        user_data = { 'user_id': user.id, 'username': user.username, 'email': user.email }
        return Response({ 'user': user_data, 'message': 'success' }, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({'message': 'Something went wrong !'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_forgot_password_request_body()
)
@api_view(['POST'])
def forgot_password_request(request):
    """
    API endpoint to reset password.

    Parameters:
        - email (string): The email of user.
    Returns:
        - 201 Created: Password Reset email sent.
        - 400 Bad Request: Invalid data provided/Some error occured.
    """
    try:
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            user.password_reset_token = token
            user.password_reset_token_expiry = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
            user.save()
            # Send email with reset link
            reset_link = f'http://localhost:3000/reset-password/{token}/'
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                'vsareen24@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        return Response({'message': 'Something went wrong !'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_reset_password_request_body()
)
@api_view(['POST'])
def reset_password(request):
    """
    API endpoint to reset password.

    Parameters:
        - token (string): The token provided.
        - password: The new password set by user.
    Returns:
        - 201 Created: Password Reset successful.
        - 400 Bad Request: Invalid data provided/Some error occured.
    """
    try:
        password = request.data.get('password')
        token = request.data.get('token')
        user = User.objects.filter(password_reset_token=token).first()

        now = timezone.localtime(timezone.now())

        if user and user.password_reset_token_expiry > now:
            user.set_password(password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return Response({'message': 'Something went wrong !'}, status=status.HTTP_400_BAD_REQUEST)
