import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

class NewsListPage(BasePage):
    
    @allure.step("Получить список новостей")
    def get_news_cards(self):
        return self.page.locator(".card")

    @allure.step("Получить количество новостей на странице")
    def get_news_count(self) -> int:
        return self.get_news_cards().count()

    @allure.step("Кликнуть по новости: {title}")
    def click_news(self, title: str):
        self.page.get_by_text(title, exact=False).first.click()

    @allure.step("Поиск новости: {query}")
    def search(self, query: str):
        search_input = self.page.get_by_placeholder("Поиск...")
        search_input.fill(query)
        search_input.press("Enter")
        self.page.wait_for_timeout(500)

    @allure.step("Перейти на страницу {page_num}")
    def go_to_page(self, page_num: int):
        self.page.get_by_role("button", name=str(page_num)).click()

    @allure.step("Проверить наличие кнопки пагинации")
    def should_have_pagination(self):
        expect(self.page.locator(".join").last).to_be_visible()

    @allure.step("Получить все теги на странице")
    def get_all_tags(self):
        return self.page.locator(".badge-outline").all_text_contents()

    @allure.step("Проверить, что есть новости")
    def should_have_news(self, min_count: int = 1):
        expect(self.get_news_cards().first).to_be_visible()
        assert self.get_news_count() >= min_count