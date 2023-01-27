from drf_yasg import openapi


login_post = {
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