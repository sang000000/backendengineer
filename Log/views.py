from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SignupSerializers , SignupRequestSerializer, LoginRequestSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_yasg.utils import swagger_auto_schema






class signup(APIView):
    """
    회원가입 API
    ---
    새로운 사용자를 등록하는 엔드포인트입니다.

    ### 사용 방법
    1. `username`, `nickname`, `password`를 입력하여 회원가입 요청을 보냅니다.
    2. 성공적으로 회원가입이 완료되면, 저장된 사용자 정보를 반환합니다.

    ### 요청 예시
    ```json
    {
        "username": "testuser",
        "nickname": "tester",
        "password": "testpassword"
    }
    ```

    ### 응답 예시 (회원가입 성공)
    ```json
    {
        "username": "testuser",
        "nickname": "tester",
        "roles": [
            {
                "role": "USER"
            }
        ]
    }
    ```

    ### 오류 응답 예시 (중복된 username)
    ```json
    {
        "username": [
            "user with this username already exists."
        ]
    }
    ```
    """
    
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignupRequestSerializer,
    )


    def post(self, request):
        
        serializer = SignupSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class Login(APIView):
    """
    로그인 API
    ---
    사용자가 아이디와 비밀번호를 입력하면 JWT Access Token과 Refresh Token을 발급합니다.

    ### 사용 방법
    1. `username`과 `password`를 입력하여 로그인 요청을 보냅니다.
    2. 올바른 사용자 정보라면, Access Token을 응답으로 반환합니다.
    3. 발급된 Access Token을 이용하여 인증이 필요한 API를 호출할 수 있습니다.

    ### 요청 예시
    ```json
    {
        "username": "testuser",
        "password": "testpassword"
    }
    ```

    ### 응답 예시 (로그인 성공)
    ```json
    {
        "token": "eyJhbGciOiJIUzI1NiIs..."
    }
    ```

    ### 오류 응답 예시 (잘못된 비밀번호)
    ```json
    {
        "detail": "username 또는 password가 틀렸습니다."
    }
    ```
    """

    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginRequestSerializer,
    )

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
    """
    Access Token 검증 API
    ---
    이 API는 발급된 Access Token이 유효한지 검증하는 엔드포인트입니다.

    ### 사용 방법
    1. 로그인 후 발급된 Access Token을 복사합니다.
    2. Swagger UI에서 **Authorize** 버튼을 클릭합니다.
    3. `Bearer <토큰>` 형식으로 Access Token을 입력하고 **Authorize**를 누릅니다.
    4. `/accessverification/` 엔드포인트를 실행하면, 정상적인 토큰이라면 인증 성공 응답을 받습니다.

    ### 응답 예시
    ```json
    {
        "message": "정상적으로 Access Token이 발급 되셨어요"
    }
    ```

    ### 오류 응답 예시 (토큰이 없거나 잘못된 경우)
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```
    """
    permission_classes = [IsAuthenticated]
    

    @swagger_auto_schema(
        security=[{"Bearer": []}],  # ✅ Swagger에서 Bearer Token 입력란 표시
        responses={200: "정상적으로 Access Token이 발급 되셨어요"}
    )
    def post(self, request):
        return Response({"정상적으로 Access Token이 발급 되셨어요"})
    

class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh Token을 사용한 Access Token 재발급 API
    ---
    로그인 후 발급받은 Refresh Token을 사용하여 새로운 Access Token을 발급합니다.

    ### 사용 방법
    1. 로그인 후 발급된 Refresh Token을 복사합니다.
    2. `/token/refresh/` 엔드포인트에 `refresh` 값을 포함하여 요청을 보냅니다.
    3. 정상적인 Refresh Token이라면 새로운 Access Token을 반환합니다.

    ### 요청 예시
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIs..."
    }
    ```

    ### 응답 예시 (토큰 재발급 성공)
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIs...",
        "refresh": "eyJhbGciOiJIUzI1NiIs..."
    }
    ```

    ### 오류 응답 예시 (Refresh Token 만료)
    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    @swagger_auto_schema(request_body=TokenRefreshSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
