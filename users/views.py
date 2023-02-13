from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from users.models import User
from users.serializers import LoginSeiralizer, SignUpSeiralizer, MyInfoSerializer
from rest_framework.decorators import api_view,permission_classes

from drf_yasg.utils import swagger_auto_schema
from users.openapi import login_post, signup_post, myinfo_get, myinfo_put

class SignUpView(APIView):
    """
        # 회원가입 요청을 위한 API
        ---
        ## 내용
        
        ### Request Body
        - **email** : 이메일 (ID로 사용됨)
        - **fullname** : 이름 혹은 별명
        - **password** : 비밀번호
    """
    serializer_class = SignUpSeiralizer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary=signup_post["operation_summary"],
        operation_id=signup_post["operation_id"],
        request_body=signup_post["request_body"], 
        responses=signup_post["responses"]
    )
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return Response({
                'access': access,
                'refresh': refresh}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
        # 로그인 요청을 위한 API
        ---
        ## 내용

        ### Request Body 
        - **email** : 이메일 (ID로 사용됨)
        - **password** : 비밀번호
    """
    serializer_class = LoginSeiralizer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary=login_post["operation_summary"],
        operation_id=login_post["operation_id"],
        request_body=login_post["request_body"], 
        responses=login_post["responses"]
    )
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
    parser_classes = [MultiPartParser]
    serializer_class = MyInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary=myinfo_get["operation_summary"],
        operation_id=myinfo_get["operation_id"],
        responses=myinfo_get["responses"],
    ) 
    def get(self, request):
        """
            # 내정보 조회를 위한 API
            ---
            ## 내용
            ### Response Body
            - **email** : 이메일 (ID로 사용됨)
            - **fullname** : 이름
            - **phone** : 휴대전화
            - **picture** : 프로필 사진
        """
        info = User.objects.filter(email=request.user)
        serializer = self.serializer_class(info, many=True)
    
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary=myinfo_put["operation_summary"],
        operation_id=myinfo_put["operation_id"],
        request_body=myinfo_put["request_body"], 
        responses=myinfo_put["responses"],
    ) 
    def put(self, request):
        """
            # 내정보 수정을 위한 API
            ---
            ## 내용
            ### Response Body
            - **email** : 이메일 (ID로 사용됨)
            - **fullname** : 이름
            - **phone** : 휴대전화
            - **picture** : 프로필 사진
        """
        info = User.objects.get(email=request.user)
        serializer = self.serializer_class(info, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        """
            # 내정보 중 특정 데이터 수정을 위한 API
            ---
            ## 내용
            ### Path Parameter
            - **picture** : 프로필 사진
            - **withdrawal** : 회원 탈퇴
        """
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