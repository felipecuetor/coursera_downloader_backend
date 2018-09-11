from django.contrib.auth.models import User, Group
from file_manager_v1.models import File, Tag, CourseXTag, Course
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
        fields = ('id','file_name','file_directory','file_course_location')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name', 'tag_importance')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('course_name','course_download_date', 'course_revised')

class CourseXTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseXTag
        fields = ('course_id','tag_id')
