import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

class RegisterPage(BasePage):
    
    @allure.step("Заполнить форму регистрации")
    def fill_form(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        self.page.locator('input[name="first_name"]').fill(first_name)
        self.page.locator('input[name="last_name"]').fill(last_name)
        self.page.locator('input[name="email"]').fill(email)
        self.page.locator('input[name="phone"]').fill(phone)
        self.page.locator('input[name="password"]').fill(password)

    @allure.step("Нажать Зарегистрироваться")
    def submit(self):
        self.page.get_by_role("button", name="Зарегистрироваться").click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Зарегистрировать пользователя")
    def register(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        self.fill_form(first_name, last_name, email, phone, password)
        self.take_screenshot("register.png")
        self.submit()

    @allure.step("Проверить сообщение об ошибке")
    def should_see_error(self):
        expect(self.page.locator(".alert-error")).to_be_visible()

    @allure.step("Проверить редирект")
    def check_redirect(self):
        expect(self.page.get_by_role("button", name="Войти")).to_be_visible()
