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
    user = User.objects.create_user('michal', 'test@scvconsultants.com', "michalpassword")
    profile_url = reverse('profile-detail', args=[user.id])
    user_url = reverse('user-detail', args=[user.id])

    # check that profile was created for created user
    response = api_client.get(profile_url)
    assert response.status_code == 200
    assert response.data['user'].endswith(user_url)

    #create bio
    bio_data = {
        "user": response.data['user'],
        "bio": "This is test user",
        "location": "Wroclaw"
    }
    #create login data as user.password contains now encrypted string
    login_data = {
        "username": user.username,
        "password": "michalpassword"
    }

    # get token
    token_url = reverse('token_obtain_pair')
    token = api_client.post(token_url, login_data, format='json')
    # check that access token was sent in response
    assert token.data['access'] is not None
    # add http authorization header with Bearer prefix
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
    # update profile
    response = api_client.put(profile_url, bio_data, format='json')
    # validate response
    assert response.status_code == 200
    assert response.data['bio'] == bio_data['bio']
    assert response.data['location'] == bio_data['location']


@pytest.mark.django_db
def test_user_create_creates_profile():
    user = User.objects.create_user('michal', 'test@scvconsultants.com', 'michalpassword')
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1
