import pytest
import allure
import uuid
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.news_list_page import NewsListPage

@allure.epic("Аутентификация")
@allure.feature("Полный цикл")
class TestAuthFlow:

    @allure.story("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_new_user(self, page):
        register_page = RegisterPage(page)
        register_page.navigate("/register")
        
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        register_page.register(
            first_name="Test",
            last_name="User",
            email=unique_email,
            phone="+79990001122",
            password="password123"
        )
        
        # Should redirect to login
        assert "/login" in page.url
        register_page.take_screenshot("after_registration")

    @allure.story("Вход с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, page):
        login_page = LoginPage(page)
        login_page.navigate("/login")
        login_page.login("test@example.com", "password123")
        
        # Should redirect to main page
        assert page.url.rstrip("/") in ["http://localhost:5137/", "http://localhost:5137"]
        login_page.take_screenshot("after_login")

    @allure.story("Вход с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, page):
        login_page = LoginPage(page)
        login_page.navigate("/login")
        login_page.login("test@example.com", "wrongpassword")
        login_page.should_see_error()

    @allure.story("Вход с несуществующим email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_nonexistent_email(self, page):
        login_page = LoginPage(page)
        login_page.navigate("/login")
        login_page.login("nonexistent@example.com", "password123")
        login_page.should_see_error()

    @allure.story("Полный цикл: регистрация → вход")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_auth_cycle(self, page):
        # Register
        register_page = RegisterPage(page)
        register_page.navigate("/register")
        unique_email = f"cycle_{uuid.uuid4().hex[:8]}@example.com"
        password = "password123"
        register_page.register("Cycle", "User", unique_email, "", password)
        
        # Login
        login_page = LoginPage(page)
        login_page.login(unique_email, password)
        
        # Verify we're logged in
        news_list = NewsListPage(page)
        news_list.navigate("/")
        expect(page.get_by_role("button", name="+ Добавить новость")).to_be_visible()