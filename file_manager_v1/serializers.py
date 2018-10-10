from django.contrib.auth.models import User, Group
from file_manager_v1.models import File, Tag, Lesson_Tag, Course, CourseLanguage, Lesson
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
        fields = ('id','file_name','file_directory','file_course_location','course_id','lesson_id')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','tag_name', 'tag_importance')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_download_date', 'course_revised', 'course_download_available', 'course_error')

class Lesson_TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson_Tag
        fields = ('id','lesson_id_number','tag_id_number')

class CourseLanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseLanguage
        fields = ('id','course_id','language')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id','lesson_name','lesson_identifier','next_lesson_id','course_id')
