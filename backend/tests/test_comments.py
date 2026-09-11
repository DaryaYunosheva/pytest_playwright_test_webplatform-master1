import pytest
import allure

@allure.feature("Комментарии")
@allure.story("Работа с комментариями")
class TestComments:

    @allure.title("Создание комментария")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_comment(self, client, auth_headers, test_news):
        response = client.post(
            f"/api/news/{test_news.id}/comments",
            headers=auth_headers,
            json={"text": "Great news!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Great news!"

    @allure.title("Создание комментария без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_comment_unauthorized(self, client, test_news):
        response = client.post(
            f"/api/news/{test_news.id}/comments",
            json={"text": "Unauthorized comment"}
        )
        
        assert response.status_code == 401

    @allure.title("Создание комментария к несуществующей новости")
    @allure.severity(allure.severity_level.NORMAL)
    def test_comment_nonexistent_news(self, client, auth_headers):
        response = client.post(
            "/api/news/99999/comments",
            headers=auth_headers,
            json={"text": "Comment"}
        )
        
        assert response.status_code == 404

    @allure.title("Получение комментариев")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_comments(self, client, test_news, test_comment):
        response = client.get(f"/api/news/{test_news.id}/comments")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @allure.title("Получение комментариев к несуществующей новости")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_comments_nonexistent(self, client):
        response = client.get("/api/news/99999/comments")
        
        assert response.status_code == 404

    @allure.title("Создание комментария с пустым текстом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_comment(self, client, auth_headers, test_news):
        response = client.post(
            f"/api/news/{test_news.id}/comments",
            headers=auth_headers,
            json={"text": ""}
        )
        
        assert response.status_code == 200  # Or 422 if validation is added