import allure
from playwright.sync_api import Page, expect
from .base_page import BasePage

class ProfilePage(BasePage):
    
    @allure.step("Заполнить имя")
    def fill_first_name(self, value: str):
        self.page.locator('input[name="first_name"]').fill(value)

    @allure.step("Заполнить фамилию")
    def fill_last_name(self, value: str):
        self.page.locator('input[name="last_name"]').fill(value)

    @allure.step("Заполнить email")
    def fill_email(self, value: str):
        self.page.locator('input[name="email"]').fill(value)

    @allure.step("Заполнить телефон")
    def fill_phone(self, value: str):
        self.page.locator('input[name="phone"]').fill(value)

    @allure.step("Загрузить фото")
    def upload_photo(self, file_path: str):
        self.page.locator('input[type="file"]').set_input_files(file_path)

    @allure.step("Сохранить профиль")
    def save(self):
        self.page.get_by_role("button", name="Сохранить").click()
        self.page.wait_for_timeout(1000)

    @allure.step("Проверить сообщение об успехе")
    def should_see_success(self):
        expect(self.page.locator(".alert-success")).to_be_visible()

    @allure.step("Проверить фото видно")
    def should_see_photo(self):
        expect(self.page.locator(".avatar img, .avatar-placeholder img, img[alt='Фото']").first).to_be_visible()