import pytest
import allure
from app.models import News, Tag

@allure.feature("Новости")
@allure.story("Получение новостей")
class TestGetNews:

    @allure.title("Получение списка новостей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_news_list(self, client, test_news):
        response = client.get("/api/news/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["total"] >= 1
        assert len(data["items"]) >= 1

    @allure.title("Пагинация новостей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_news_pagination(self, client, db_session, test_user):
        # Create 15 news items
        for i in range(15):
            news = News(
                title=f"News {i}",
                text=f"Content {i}",
                author_id=test_user.id
            )
            db_session.add(news)
        db_session.commit()
        
        # Test page 1
        response_page1 = client.get("/api/news/?page=1&per_page=10")
        assert response_page1.status_code == 200
        assert len(response_page1.json()["items"]) == 10
        
        # Test page 2
        response_page2 = client.get("/api/news/?page=2&per_page=10")
        assert response_page2.status_code == 200
        assert len(response_page2.json()["items"]) >= 5

    @allure.title("Поиск новостей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_news(self, client, test_news):
        response = client.get("/api/news/?search=Test News")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    @allure.title("Фильтрация по тегам")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_tag(self, client, db_session, test_user, test_news):
        tag = Tag(name="technology")
        db_session.add(tag)
        test_news.tags.append(tag)
        db_session.commit()
        
        response = client.get("/api/news/?tag=technology")
        
        assert response.status_code == 200
        assert response.json()["total"] >= 1

    @allure.title("Получение деталей новости")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_news_detail(self, client, test_news):
        response = client.get(f"/api/news/{test_news.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_news.id
        assert data["title"] == "Test News Title"

    @allure.title("Получение несуществующей новости")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_news(self, client):
        response = client.get("/api/news/99999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "News not found"


@allure.feature("Новости")
@allure.story("Создание новостей")
class TestCreateNews:

    @allure.title("Создание новости с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_news_authenticated(self, client, auth_headers):
        response = client.post("/api/news/", headers=auth_headers, data={
            "title": "New Test News",
            "subtitle": "Test Subtitle",
            "text": "This is a new test news content.",
            "tags": "test, news"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Test News"
        assert len(data["tags"]) == 2

    @allure.title("Создание новости без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_news_unauthenticated(self, client):
        response = client.post("/api/news/", data={
            "title": "Unauthorized News",
            "text": "Should not be created"
        })
        
        assert response.status_code == 401

    @allure.title("Создание новости без обязательных полей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_news_missing_fields(self, client, auth_headers):
        response = client.post("/api/news/", headers=auth_headers, data={})
        
        assert response.status_code == 422

    @allure.title("Создание новости с изображением")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_news_with_image(self, client, auth_headers):
        import io
        
        image_content = io.BytesIO(b"fake image content")
        files = {"image": ("test_image.jpg", image_content, "image/jpeg")}
        data = {
            "title": "News with Image",
            "text": "Content with image"
        }
        
        response = client.post("/api/news/", headers=auth_headers, data=data, files=files)
        
        assert response.status_code == 200
        assert response.json()["image_path"] is not None