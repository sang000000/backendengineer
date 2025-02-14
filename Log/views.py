from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SignupSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse




class signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class Login(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            

            # 로그인 상태 유지
            login(request, user)

            return Response({"token": access_token})
        return Response({"username 또는 password가 틀렸습니다"})

class AccessVerification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"정상적으로 Access Token이 발급 되셨어요"})
