import pytest
from django.urls import reverse
from movies.models import Movie


@pytest.mark.django_db
def test_home_page_random_movie(client):
    # Создаем несколько фильмов
    Movie.objects.create(title="Movie 1", review="Great movie!", poster="poster1.jpg")
    Movie.objects.create(title="Movie 2", review="Not bad", poster="poster2.jpg")

    # Делаем запрос на главную страницу
    url = reverse("home")
    response = client.get(url)

    # Проверяем, что страница загружается успешно
    assert response.status_code == 200
    assert "movie" in response.context  # movie должен быть в контексте
    assert response.context["movie"].title in ["Movie 1", "Movie 2"]
    assert response.context["movie"].review in ["Great movie!", "Not bad"]


@pytest.mark.django_db
def test_movie_creation(client):
    # Проверяем, что можно создать фильм
    movie = Movie.objects.create(
        title="Movie 1", review="Great movie!", poster="poster1.jpg"
    )
    assert Movie.objects.filter(title="Movie 1").exists()
    assert movie.review == "Great movie!"
    assert movie.poster == "poster1.jpg"
