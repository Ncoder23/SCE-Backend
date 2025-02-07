from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserRegistrationSerializer, UserLoginSerializer
import re
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        # Check if all required fields are present
        required_fields = ['email', 'password',
                           'first_name', 'last_name', 'phone_number']
        missing_fields = [
            field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Validate password strength
            password = serializer.validated_data['password']
            if not self.validate_password(password):
                return Response({
                    'error': 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate phone number format
            phone_number = serializer.validated_data.get('phone_number')
            if not self.validate_phone_number(phone_number):
                return Response({
                    'error': 'Invalid phone number format. Please use format: +1234567890'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if email already exists
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({
                    'error': 'Email already registered'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'User registered successfully',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    },
                    'token': token.key
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': f'Error creating user: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def validate_password(password):
        """
        Validate that password meets minimum requirements:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character
        """
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    @staticmethod
    def validate_phone_number(phone):
        """
        Validate phone number format
        Accepts formats like: +1234567890
        """
        if not phone:
            return False
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        return bool(phone_pattern.match(phone))


@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'email': user.email
                }, status=status.HTTP_200_OK)

            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # print("LogoutUserView called")
            # print(request.user)
            # Delete the user's token to logout
            request.user.auth_token.delete()
            logout(request)
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
