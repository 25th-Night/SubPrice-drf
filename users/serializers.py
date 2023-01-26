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

    def create(self, validated_data):
        email = validated_data['email']
        fullname = validated_data['fullname']
        password = validated_data['password']

        user = User.objects.create(email=email, fullname=fullname)
        user.set_password(password)
        user.save()

        return user

class LoginSeiralizer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate(self, data):
        error = {}

        email = data.get('email', None)
        password = data.get('password', None)

        user = User.objects.filter(email=email).last()

        if not user:
            error["email"] = "올바른 이메일 주소를 입력해주세요."

        elif not user.is_active:
            error["email"] = "탈퇴한 회원입니다."

        elif not user.check_password(password):
            error["password"] = "잘못된 비밀번호입니다. 다시 확인하세요."

        if error:
            raise serializers.ValidationError(error)

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

    def update(self, instance, validated_data):
        instance.email  = validated_data.get('email', instance.email)
        instance.fullname = validated_data.get('fullname',  instance.fullname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.password = validated_data.get('password', instance.password)
        
        instance.set_password(instance.password)
        instance.save()

        return instance