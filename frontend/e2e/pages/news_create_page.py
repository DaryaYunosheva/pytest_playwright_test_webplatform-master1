import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

class NewsCreatePage(BasePage):
    
    @allure.step("Заполнить заголовок")
    def fill_title(self, title: str):
        self.page.locator('input[name="title"]').fill(title)

    @allure.step("Заполнить подзаголовок")
    def fill_subtitle(self, subtitle: str):
        self.page.locator('input[name="subtitle"]').fill(subtitle)

    @allure.step("Заполнить текст")
    def fill_text(self, text: str):
        self.page.locator('textarea[name="text"]').fill(text)

    @allure.step("Заполнить теги")
    def fill_tags(self, tags: str):
        self.page.locator('input[name="tags"]').fill(tags)

    @allure.step("Загрузить изображение")
    def upload_image(self, file_path: str):
        self.page.locator('input[type="file"]').set_input_files(file_path)

    @allure.step("Нажать кнопку Создать")
    def submit(self):
        self.page.get_by_role("button", name="Создать").click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Создать новость полностью")
    def create_news(self, title: str, text: str, subtitle: str = "", tags: str = ""):
        self.fill_title(title)
        if subtitle:
            self.fill_subtitle(subtitle)
        self.fill_text(text)
        if tags:
            self.fill_tags(tags)
        self.submit()