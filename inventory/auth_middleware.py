import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('calling the middleware function')

        paths_to_skip_csrf = [
            '/swagger/',
            '/admin/',
            '/api/login',
            '/api/create-account',
            '/api/forgot-password',
            '/api/reset-password',
        ]

        # Check if the request path is in the list of paths to skip CSRF
        if request.path in paths_to_skip_csrf:
            # Skip CSRF protection for these paths
            response = self.get_response(request)
            return response

        # Get the JWT token from the request
        token = request.headers.get('token')

        if token:
            try:
                # Decode and verify the token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                # Add the decoded token payload to the request for later use
                request.jwt_payload = payload
            except jwt.ExpiredSignatureError:
                # Token has expired

                return JsonResponse({
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Token has expired'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            except jwt.InvalidTokenError:
                # Token is invalid
                return JsonResponse({
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Please provide Token'
            }, status=status.HTTP_401_UNAUTHORIZED)


        # Call the next middleware or view function
        response = self.get_response(request)
        return response
        