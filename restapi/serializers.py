from django.contrib.auth.models import User
from rest_framework import serializers

from restapi.models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'birth_date', 'days']