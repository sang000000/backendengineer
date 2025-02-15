from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["role"]

class SignupRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ["username", "nickname", "password"]  # 🔥 요청에서는 password 포함

class SignupResponseSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["username", "nickname", "roles"]  # ✅ 응답에서는 password 제거

class SignupSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "password",
            
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")  # 비밀번호 따로 저장
        user = User(**validated_data)
        user.set_password(password)  # 비밀번호 암호화
        user.roles, _ = Role.objects.get_or_create(role="USER")  # 🔹 roles를 자동으로 "USER" 설정
        user.save()

        return user  # 비밀번호는 응답에 포함되지 않음
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # roles 값 포맷을 맞추기 위해 재구성
        representation['roles'] = [{"role": instance.roles.role}]
        return representation
    

class LoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            
        ]

