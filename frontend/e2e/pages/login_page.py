import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    
    @allure.step("Заполнить email")
    def fill_email(self, email: str):
        self.page.locator('input[type="email"]').fill(email)

    @allure.step("Заполнить пароль")
    def fill_password(self, password: str):
        self.page.locator('input[type="password"]').fill(password)

    @allure.step("Нажать Войти")
    def submit(self):
        self.page.get_by_role("button", name="Войти").click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Войти как {email}")
    def login(self, email: str, password: str):
        self.fill_email(email)
        self.fill_password(password)
        self.submit()

    @allure.step("Проверить сообщение об ошибке")
    def should_see_error(self):
        expect(self.page.locator(".alert-error")).to_be_visible()