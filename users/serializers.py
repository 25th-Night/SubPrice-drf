from rest_framework import serializers
from users.models import User
import re

class SignUpSeiralizer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    fullname = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, data):

        match = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        validation = re.compile(match)

        error = {}
        
        if User.objects.filter(email=data['email']).exists():
            error["email"] = "이미 존재하는 아이디입니다."
        if validation.match(str(data['password'])) is None:
            error["password"] = "비밀번호는 하나 이상의 문자, 숫자, 특수문자를 포함하여 8자리 이상으로 작성해주세요."

        if error:
            raise serializers.ValidationError(error)

        return data

class LoginSeiralizer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError("올바른 이메일 주소를 입력해주세요.")
        else:
            raise serializers.ValidationError("잘못된 비밀번호입니다. 다시 확인하세요.")

        return data