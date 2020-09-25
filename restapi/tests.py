import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_user_can_update_his_profile(api_client):
    user = User.objects.create_user('michal', 'test@scvconsultants.com', 'michalpassword')
    url = reverse('profile-detail', args=[user.id])
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_create_creates_profile():
    User.objects.create_user('michal', 'test@scvconsultants.com', 'michalpassword')
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1
