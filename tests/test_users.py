import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_registration(client):
    url = reverse("user-register")
    data = {
        "username": "testuser",
        "password1": "password123",
        "password2": "password123",
        "email": "testuser@example.com",
    }

    response = client.post(url, data)

    assert response.status_code == 302  # Ожидаем редирект после успешной регистрации
    assert User.objects.filter(username="testuser").exists()
    assert User.objects.filter(email="testuser@example.com").exists()


@pytest.mark.django_db
def test_user_registration_invalid(client):
    url = reverse("user-register")
    data = {
        "username": "testuser",
        "password1": "password123",
        "password2": "password124",  # Пароли не совпадают
        "email": "testuser@example.com",
    }

    response = client.post(url, data)

    assert response.status_code == 200  # Ожидаем, что форма не будет отправлена
    assert (
        "password2" in response.context["form"].errors
    )  # Ошибка на поле повторного пароля
