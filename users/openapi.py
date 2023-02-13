from drf_yasg import openapi
from users.serializers import MyInfoSerializer

login_post = {
    "operation_summary" : "로그인 요청",
    "operation_id" : '로그인',
    "request_body" : openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        operation_id='일반 회원가입',
        operation_description='회원가입을 진행합니다.',
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, title='Email', description='이메일'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, title='Password', description='비밀번호'),
        },
        required=['email', 'password']
    ),
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
                }
            )
        ), 
        422: openapi.Response(
            description="Not found or Not accessible", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="이메일 검증 오류 메세지"),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호 검증 오류 메세지"),
                }
            )
        )
    }
}

signup_post = {
    "operation_summary" : "회원가입 요청",
    "operation_id" : '회원가입',
    "request_body" : openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        operation_id='일반 회원가입',
        operation_description='회원가입을 진행합니다.',
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, title='Email', description='이메일'),
            'fullname': openapi.Schema(type=openapi.TYPE_STRING, title='Fullname', description='이름'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, title='Password', description='비밀번호'),
        },
        required=['email','fullname', 'password']
    ),
    "responses" : {
        201: openapi.Response(
            description="Created", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
                }
            )
        ), 
        422: openapi.Response(
            description="Not found or Not accessible", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="이메일 검증 오류 메세지"),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호 검증 오류 메세지"),
                }
            )
        )
    }
}

myinfo_get = {
    "operation_summary" : "내정보 조회",
    "operation_id" : '내정보 조회',
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, title='Email', description='이메일'),
                    'fullname': openapi.Schema(type=openapi.TYPE_STRING, title='Fullname', description='이름'),
                    'phone': openapi.Schema(type=openapi.TYPE_STRING, title='Phone', description='휴대폰'),
                    'picture': openapi.Schema(type=openapi.TYPE_STRING, title='Picture', description='프로필 사진'),
                },
                required=['email','fullname']
            )
        ),
        401: openapi.Response(
            description="Unauthorized", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="권한 오류 메세지"),
                }
            )
        )
    }
}


myinfo_put = {
    "operation_summary" : "내정보 수정",
    "operation_id" : '내정보 수정',
    "request_body" : MyInfoSerializer,
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="정상"),
                }
            )
        ),
        400: openapi.Response(
            description="Bad Request", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'phone': openapi.Schema(type=openapi.TYPE_STRING, description="휴대폰 검증 오류 메세지"),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호 검증 오류 메세지"),
                }
            )
        )
    }
}


myinfo_patch = {
    "operation_summary" : "내정보 일부 수정",
    "operation_id" : '내정보 중 특정 데이터 수정',
    "manual_parameters" : [
        openapi.Parameter(
            "picture",
            openapi.IN_QUERY,
            description="`remove` 요청 시, 프로필 사진 삭제.",
            type=openapi.TYPE_STRING,
            enum=['remove'],
        ),
        openapi.Parameter(
            "withdrawal",
            openapi.IN_QUERY,
            description="`yes` 요청 시, 내계정 비활성화(탈퇴 처리).",
            type=openapi.TYPE_STRING,
            enum=['yes'],
        ),
    ],
    "responses" : {
        200: openapi.Response(
            description="Success", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="정상"),
                }
            )
        ),
        400: openapi.Response(
            description="Bad Request", 
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description="잘못된 요청입니다."),
                }
            )
        )
    }
}