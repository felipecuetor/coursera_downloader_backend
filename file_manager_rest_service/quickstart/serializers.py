from django.contrib.auth.models import User, Group
from quickstart.models import File
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('file_name','file_directory')
