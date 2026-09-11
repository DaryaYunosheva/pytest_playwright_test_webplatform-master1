import pytest
import allure
import uuid
from pages.login_page import LoginPage
from pages.news_create_page import NewsCreatePage
from pages.news_list_page import NewsListPage

@allure.epic("Новости")
@allure.feature("Создание новости")
class TestNewsCreate:

    @pytest.fixture(autouse=True)
    def login(self, page):
        """Выполняется перед каждым тестом."""
        login_page = LoginPage(page)
        login_page.navigate("/login")
        login_page.login("test@example.com", "password123")

    @allure.story("Создание новости без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_news_requires_auth(self, page):
        page.context.clear_cookies()
        create_page = NewsCreatePage(page)
        create_page.navigate("/news/create")
        assert "/login" in page.url

    @allure.story("Создание новости с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_news_success(self, page):
        create_page = NewsCreatePage(page)
        create_page.navigate("/news/create")
        
        unique_title = f"Новость {uuid.uuid4().hex[:6]}"
        create_page.create_news(
            title=unique_title,
            subtitle="Подзаголовок теста",
            text="Это текст тестовой новости для проверки создания.",
            tags="тест, pytest"
        )
        
        # Should redirect to main page
        assert "/news/create" not in page.url
        create_page.take_screenshot("after_news_creation")
        
        # Verify news appears in list
        news_list = NewsListPage(page)
        news_list.navigate("/")
        assert page.get_by_text(unique_title).first.is_visible()

    @allure.story("Создание новости без заголовка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_news_no_title(self, page):
        create_page = NewsCreatePage(page)
        create_page.navigate("/news/create")
        
        create_page.fill_text("Текст без заголовка")
        create_page.submit()
        
        # Should show validation error
        assert page.locator('input[name="title"]:invalid').count() > 0

    @allure.story("Создание новости без текста")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_news_no_text(self, page):
        create_page = NewsCreatePage(page)
        create_page.navigate("/news/create")
        
        create_page.fill_title("Заголовок без текста")
        create_page.submit()
        
        # Should show validation error
        assert page.locator('textarea[name="text"]:invalid').count() > 0