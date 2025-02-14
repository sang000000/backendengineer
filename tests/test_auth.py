import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()



@pytest.fixture
def api_client():
    """ API 요청을 위한 클라이언트 """
    return APIClient()

@pytest.fixture
def test_sinup_and_login(api_client):
    response = api_client.post("/accounts/signup/",{"username": "test", "password": "zxcv12345", "nickname" : "tt"})
    assert response.status_code == 201
    assert User.objects.filter(username="test").exists()
    assert response.data == {
        "username": "test",
        "nickname": "tt",
        "roles":[ 
			{
					"role": "USER"
			}
        ]
    }

    login_response = api_client.post("/accounts/login/", {"username": "test", "password": "zxcv12345"})
    assert login_response.status_code == 200
    assert "token" in login_response.data  # Access Token이 포함되어 있는지 확인
    return {
        "access": login_response.data["token"],  
        "refresh": str(RefreshToken.for_user(User.objects.get(username="test")))
    }

@pytest.mark.django_db
def test_access_token(api_client,test_sinup_and_login):
    """ Access Token이 정상적으로 API 요청을 처리하는지 테스트"""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {test_sinup_and_login['access']}")  # Access Token 포함
    response = api_client.post("/accounts/accessverification/")  # 보호된 API 호출
    assert response.status_code == 200  # 인증 성공

def test_access_token_invalid(api_client):
    """ 잘못된 Access Token을 사용할 경우 401 오류가 발생하는지 테스트"""
    api_client.credentials(HTTP_AUTHORIZATION="Bearer INVALID_TOKEN")
    response = api_client.post("/accounts/accessverification/")
    assert response.status_code == 401  # 인증 실패

@pytest.mark.django_db
def test_refresh_token(api_client,test_sinup_and_login):
    """ Refresh Token을 이용해 새로운 Access Token을 발급할 수 있는지 테스트"""
    response = api_client.post("/accounts/token/refresh/", {"refresh": test_sinup_and_login['refresh']})
    assert response.status_code == 200
    assert "access" in response.data  # 새로운 Access Token이 포함되어 있는지 확인

def test_refresh_token_invalid(api_client):
    """ 잘못된 Refresh Token을 사용할 경우 401 오류가 발생하는지 테스트"""
    response = api_client.post("/accounts/token/refresh/", {"refresh": "INVALID_REFRESH_TOKEN"})
    assert response.status_code == 401  # 인증 실패