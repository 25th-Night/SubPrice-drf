from rest_framework import serializers
from users.models import User

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