from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from users.models import User

from users.serializers import LoginSeiralizer

class LoginView(APIView):

    serializer_class = LoginSeiralizer
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return Response({
                'access': access,
                'refresh': refresh}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyInfoView(APIView):
    pass