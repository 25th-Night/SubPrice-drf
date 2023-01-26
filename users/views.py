from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from users.serializers import LoginSeiralizer, SignUpSeiralizer, MyPageSerializer
from rest_framework.decorators import api_view,permission_classes

class SignUpView(APIView):
    serializer_class = SignUpSeiralizer
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return Response({
                'access': access,
                'refresh': refresh}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = MyPageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        info = User.objects.filter(email=request.user)
        serializer = self.serializer_class(info, many=True)
    
        return Response(serializer.data)

    def put(self, request):
        info = User.objects.get(email=request.user)
        serializer = self.serializer_class(info, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        picture = request.GET.get('picture', None)
        if picture == "remove":
            user = User.objects.get(id=request.user.id)
            print(user)
            user.picture = None
            user.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)

        withdrawal = request.GET.get('withdrawal', None)
        if withdrawal == "yes":
            user = User.objects.get(id=request.user.id)
            user.is_active = 0
            user.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response({"message": "비정상"}, status=status.HTTP_400_BAD_REQUEST)