import pytest
import allure
from pages.news_list_page import NewsListPage

@allure.epic("Новости")
@allure.feature("Пагинация")
class TestPagination:

    @allure.story("Переход по страницам")
    @allure.severity(allure.severity_level.NORMAL)
    def test_navigate_pages(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        
        # Click page 2 if exists
        page2_btn = page.get_by_role("button", name="2")
        if page2_btn.is_visible():
            page2_btn.click()
            page.wait_for_timeout(1000)
            news_list.should_have_news()

    @allure.story("Возврат к первой странице")
    @allure.severity(allure.severity_level.NORMAL)
    def test_return_to_first_page(self, page):
        news_list = NewsListPage(page)
        news_list.navigate("/")
        
        # Go to page 2
        page2_btn = page.get_by_role("button", name="2")
        if page2_btn.is_visible():
            page2_btn.click()
            page.wait_for_timeout(1000)
            
            # Return to page 1
            page1_btn = page.get_by_role("button", name="1")
            page1_btn.click()
            page.wait_for_timeout(1000)
            news_list.should_have_news()