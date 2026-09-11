import pytest
import allure
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

@allure.epic("Профиль")
@allure.feature("Управление профилем")
class TestProfile:

    @pytest.fixture(autouse=True)
    def login(self, page):
        login_page = LoginPage(page)
        login_page.navigate("/login")
        login_page.login("test@example.com", "password123")

    @allure.story("Обновление профиля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_profile(self, page):
        profile = ProfilePage(page)
        profile.navigate("/profile")
        
        profile.fill_first_name("Updated")
        profile.fill_last_name("User")
        profile.fill_phone("+79998887766")
        profile.save()
        
        profile.should_see_success()
        profile.take_screenshot("profile_updated")

    @allure.story("Загрузка фото")
    @allure.severity(allure.severity_level.NORMAL)
    def test_upload_photo(self, page):
        import tempfile
        import os
        
        # Create a tiny test image
        temp_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        temp_image.write(b'\xff\xd8\xff\xe0\x00\x10JFIF')  # Minimal JPEG header
        temp_image.close()
        
        profile = ProfilePage(page)
        profile.navigate("/profile")
        profile.upload_photo(temp_image.name)
        page.wait_for_timeout(2000)
        
        profile.take_screenshot("photo_uploaded")
        os.unlink(temp_image.name)

    @allure.story("Профиль без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_profile_requires_auth(self, page):
        page.context.clear_cookies()
        profile = ProfilePage(page)
        profile.navigate("/profile")
        assert "/login" in page.url