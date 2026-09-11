import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

class NewsDetailPage(BasePage):
    
    @allure.step("Получить заголовок новости")
    def get_news_title(self) -> str:
        return self.page.locator("h1").first.text_content()

    @allure.step("Получить комментарии")
    def get_comments(self):
        return self.page.locator(".card.bg-base-100.shadow")

    @allure.step("Добавить комментарий: {text}")
    def add_comment(self, text: str):
        textarea = self.page.get_by_placeholder("Оставьте комментарий...")
        textarea.fill(text)
        self.page.get_by_role("button", name="Отправить").click()
        self.page.wait_for_timeout(500)

    @allure.step("Проверить комментарий виден")
    def should_see_comment(self, text: str):
        expect(self.page.get_by_text(text)).to_be_visible()

    @allure.step("Проверить наличие секции комментариев")
    def should_have_comments_section(self):
        expect(self.page.get_by_text("Комментарии")).to_be_visible()

    @allure.step("Проверить наличие тегов")
    def should_have_tags(self):
        expect(self.page.locator(".badge-outline").first).to_be_visible()

    @allure.step("Проверить, что комментарий недоступен для неавторизованных")
    def should_not_see_comment_form(self):
        expect(self.page.get_by_placeholder("Оставьте комментарий...")).not_to_be_visible()