from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import status

from accounts.serializers import RegisterSerializer, UserSerializer, LoginSerializer, LogoutSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user with name, email, and password.
    """
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveAPIView):
    """
    Retrieve the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginView(generics.GenericAPIView):
    """
    Authenticate user and return JWT access and refresh tokens.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class LogoutView(generics.GenericAPIView):
    """
    Logout the user by blacklisting the refresh token.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
