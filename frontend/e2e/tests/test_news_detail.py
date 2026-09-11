import pytest
import allure
from pages.news_list_page import NewsListPage
from pages.news_detail_page import NewsDetailPage

@allure.epic("Новости")
@allure.feature("Детали новости")
class TestNewsDetail:

    @allure.story("Просмотр деталей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_news_detail(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        first_card_title = page.locator(".card-title").first.text_content()
        news_list.click_news(first_card_title)
        
        detail = NewsDetailPage(page)
        detail.should_have_comments_section()
        detail.should_have_tags()
        detail.take_screenshot("news_detail")

    @allure.story("Комментарий без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_comment_requires_auth(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        first_card_title = page.locator(".card-title").first.text_content()
        news_list.click_news(first_card_title)
        
        detail = NewsDetailPage(page)
        detail.should_not_see_comment_form()