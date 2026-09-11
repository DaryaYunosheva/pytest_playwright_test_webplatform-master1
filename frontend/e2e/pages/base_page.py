import allure
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page, base_url: str = "http://localhost:5137"):
        self.page = page
        self.base_url = base_url

    @allure.step("Перейти на {path}")
    def navigate(self, path: str = "/"):
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("networkidle")

    @allure.step("Получить заголовок страницы")
    def get_title(self) -> str:
        return self.page.title()

    @allure.step("Сделать скриншот: {name}")
    def take_screenshot(self, name: str = "screenshot"):
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot

    @allure.step("Проверить, что текст виден: {text}")
    def should_see_text(self, text: str):
        expect(self.page.get_by_text(text)).to_be_visible()
        return self

    @allure.step("Проверить, что кнопка видна: {name}")
    def should_see_button(self, name: str):
        expect(self.page.get_by_role("button", name=name)).to_be_visible()
        return self