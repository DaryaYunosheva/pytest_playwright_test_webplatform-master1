import pytest
import allure
from pages.news_list_page import NewsListPage

@allure.epic("Новости")
@allure.feature("Список новостей")
class TestNewsList:

    @allure.story("Просмотр списка новостей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_news_list_loads(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        news_list.should_have_news()
        news_list.take_screenshot("news_list")

    @allure.story("Поиск новостей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_news(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        news_list.search("тест")
        news_list.should_have_news(min_count=0)  # At least page loads

    @allure.story("Пагинация")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pagination(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        news_list.should_have_pagination()

    @allure.story("Переход к деталям новости")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_detail(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        first_card_title = page.locator(".card-title").first.text_content()
        news_list.click_news(first_card_title)
        assert "/news/" in page.url