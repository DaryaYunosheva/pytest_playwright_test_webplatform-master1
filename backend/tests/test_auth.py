import pytest
import allure
from app.models import User

@allure.feature("Аутентификация")
@allure.story("Регистрация")
class TestRegistration:

    @allure.title("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_success(self, client):
        with allure.step("Отправляем POST /api/auth/register"):
            response = client.post("/api/auth/register", json={
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "phone": "+79998887766",
                "password": "securepass123"
            })
        
        with allure.step("Проверяем статус-код 200"):
            assert response.status_code == 200
        
        with allure.step("Проверяем данные в ответе"):
            data = response.json()
            assert data["email"] == "newuser@example.com"
            assert data["first_name"] == "New"
            assert data["last_name"] == "User"
            assert "password_hash" not in data

    @allure.title("Ошибка регистрации при существующем email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_duplicate_email(self, client, test_user):
        with allure.step("Пытаемся зарегистрировать с тем же email"):
            response = client.post("/api/auth/register", json={
                "email": "test@example.com",
                "first_name": "Another",
                "last_name": "User",
                "password": "password123"
            })
        
        with allure.step("Проверяем статус-код 400"):
            assert response.status_code == 400
        
        with allure.step("Проверяем сообщение об ошибке"):
            assert response.json()["detail"] == "Email already registered"

    @allure.title("Ошибка регистрации при коротком пароле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_short_password(self, client):
        response = client.post("/api/auth/register", json={
            "email": "shortpass@example.com",
            "first_name": "Short",
            "last_name": "Pass",
            "password": "12345"
        })
        
        assert response.status_code == 422

    @allure.title("Ошибка регистрации при невалидном email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_invalid_email(self, client):
        response = client.post("/api/auth/register", json={
            "email": "invalid-email",
            "first_name": "Invalid",
            "last_name": "Email",
            "password": "password123"
        })
        
        assert response.status_code == 422


@allure.feature("Аутентификация")
@allure.story("Вход в систему")
class TestLogin:

    @allure.title("Успешный вход с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, client, test_user):
        with allure.step("Отправляем POST /api/auth/login"):
            response = client.post("/api/auth/login", data={
                "username": "test@example.com",
                "password": "testpassword123"
            })
        
        with allure.step("Проверяем статус-код 200"):
            assert response.status_code == 200
        
        with allure.step("Проверяем наличие токена"):
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

    @allure.title("Ошибка входа при неверном пароле")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, client, test_user):
        response = client.post("/api/auth/login", data={
            "username": "test@example.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"

    @allure.title("Ошибка входа при несуществующем email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_email(self, client):
        response = client.post("/api/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "somepassword"
        })
        
        assert response.status_code == 401

    @allure.title("Ошибка входа при пустых полях")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_fields(self, client):
        response = client.post("/api/auth/login", data={})
        
        assert response.status_code == 422