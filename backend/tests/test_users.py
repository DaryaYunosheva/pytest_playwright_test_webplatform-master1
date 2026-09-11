import pytest
import allure
from app.models import User

@allure.feature("Пользователи")
@allure.story("Профиль")
class TestUserProfile:

    @allure.title("Получение текущего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_current_user(self, client, auth_headers, test_user):
        response = client.get("/api/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"

    @allure.title("Получение профиля без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_current_user_unauthorized(self, client):
        response = client.get("/api/users/me")
        
        assert response.status_code == 401

    @allure.title("Обновление профиля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_profile(self, client, auth_headers):
        response = client.put("/api/users/me", headers=auth_headers, json={
            "first_name": "Updated",
            "last_name": "Name",
            "phone": "+79990001122"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
        assert data["phone"] == "+79990001122"

    @allure.title("Обновление email на занятый")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_email_conflict(self, client, auth_headers, db_session, test_user):
        # Create another user
        other_user = User(
            email="other@example.com",
            first_name="Other",
            last_name="User",
            password_hash="hash",
            is_active=True
        )
        db_session.add(other_user)
        db_session.commit()
        
        response = client.put("/api/users/me", headers=auth_headers, json={
            "email": "other@example.com"
        })
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already in use"

    @allure.title("Обновление пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_password(self, client, auth_headers):
        response = client.put("/api/users/me", headers=auth_headers, json={
            "password": "newpassword123"
        })
        
        assert response.status_code == 200
        
        # Verify new password works
        login_response = client.post("/api/auth/login", data={
            "username": "test@example.com",
            "password": "newpassword123"
        })
        assert login_response.status_code == 200

    @allure.title("Загрузка фото профиля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_upload_photo(self, client, auth_headers):
        import io
        
        photo_content = io.BytesIO(b"fake image content")
        files = {"photo": ("test_photo.jpg", photo_content, "image/jpeg")}
        
        response = client.post("/api/users/me/photo", headers=auth_headers, files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "photo_path" in data
        assert data["photo_path"] is not None