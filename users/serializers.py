from rest_framework import serializers
from users.models import User
import re

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

class MyPageSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    fullname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    picture = serializers.ImageField(use_url=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        error = {}

        match = "^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$"
        validation = re.compile(match)
        
        if validation.match(str(data['phone'])) is None:
            error["phone"] = "정확한 전화번호를 입력해주세요."
        
        match = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        validation = re.compile(match)
        
        if validation.match(str(data['password'])) is None:
            error["password"] = "비밀번호는 하나 이상의 문자, 숫자, 특수문자를 포함하여 8자리 이상으로 작성해주세요."

        if error:
            raise serializers.ValidationError(error)

        return data