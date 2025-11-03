import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Organization
# Create your tests here.
User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser2", email='admin@gmail.com', password="pass123", first_name='user2', phone="9851632233")


@pytest.mark.django_db
def test_create_organization(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("organization-list-create")
    data = {"name": "MyOrg", "description": "Testing fixtures"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "MyOrg"


@pytest.mark.django_db
def test_create_org_unauthenticated_user(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('organization-list-create')
    response = api_client.get(url)

    assert response.status_code == 200
