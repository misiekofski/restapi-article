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
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1

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
def test_user_should_not_be_able_to_update_other_profile(api_client):
    first_user = User.objects.create_user('michal', 'test@scvconsultants.com', "michalpassword")
    second_user = User.objects.create_user('michal2', 'test2@scvconsultants.com', "michalpassword2")
    assert Profile.objects.count() == User.objects.count()

    #get token for first_user
    token_url = reverse('token_obtain_pair')
    login_data = {
        "username": first_user.username,
        "password": "michalpassword"
    }
    token = api_client.post(token_url, login_data, format='json')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
    # now update second_user Profile with first_user token
    profile_url = reverse('profile-detail', args=[second_user.id])
    response = api_client.get(profile_url)
    bio_data = {
        "user": response.data['user'],
        "bio": "This is test user",
        "location": "Wroclaw"
    }
    response = api_client.put(profile_url, bio_data, format='json')
    g
