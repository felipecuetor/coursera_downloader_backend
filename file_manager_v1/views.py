# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from file_manager_v1.models import File, Tag, Lesson_Tag, Course, CourseLanguage, Lesson
from file_manager_v1.serializers import LessonSerializer, UserSerializer, GroupSerializer, FileSerializer, TagSerializer, Lesson_TagSerializer, CourseSerializer,CourseLanguageSerializer
from utils.file_manager_utils import directory_recursive_generator
import json

# Create your views here.

class FileDetail(APIView):
    """
    Retrieve, update or delete a file instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        original_file_serializer = FileSerializer(file)
        file_new_location = {}
        file_new_location["file_course_location"]=request.data["file_course_location"]
        file_new_location["id"] = original_file_serializer.data["id"]
        file_new_location["file_directory"] = original_file_serializer.data["file_directory"]
        file_new_location["file_name"] = original_file_serializer.data["file_name"]
        serializer = FileSerializer(file, data=file_new_location)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def downloadCourse(request):
    print(request.method)
    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
    if request.method == 'POST':
        print("Download Request recieved")
        course_name = request.data["course_name"]
        username = request.data["username"]
        password = request.data["password"]
        course_download_thread_generator(username, password, course_name, 1)
        return Response(status=status.HTTP_200_OK)

class MoveFileView(APIView):
    """
    Retrieve, update or delete a file instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        original_file_serializer = FileSerializer(file)
        file_location = request.GET.get('file_course_location')
        file_new_location = {}
        file_new_location["file_course_location"]=file_location
        file_new_location["id"] = original_file_serializer.data["id"]
        file_new_location["file_directory"] = original_file_serializer.data["file_directory"]
        file_new_location["file_name"] = original_file_serializer.data["file_name"]
        serializer = FileSerializer(file, data=file_new_location)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecificCourseToggleRevised(APIView):
    def get_object(self, course_id):
        try:
            return Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        course = self.get_object(course_id)
        original_course_serializer = CourseSerializer(course)
        change_course = original_course_serializer.data
        change_course["course_revised"] = not change_course["course_revised"]
        serializer = CourseSerializer(course, data=change_course)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecificLessonTagsView(APIView):
    #Retrieve, update or delete a Lesson_Tag instance.
    def get_all_lesson_tags(self, lesson_id):
        try:
            return Lesson_Tag.objects.filter(lesson_id_number=lesson_id)
        except:
            raise Http404

    def get(self, request, format=None):
        lesson_id = request.GET.get('lesson_id')
        lesson_x_tag = self.get_all_lesson_tags(lesson_id)
        json_response=[]
        for tag in lesson_x_tag.values():
            tag_query=Tag.objects.filter(id=tag["tag_id_number"])
            tag_object={
                "id":tag["id"],
                "tag_name":tag_query.values()[0]["tag_name"],
                "tag_id_number":tag["tag_id_number"]
            }
            json_response.append(tag_object)
        print json_response
        return Response(json_response)

class LessonListTagsView(APIView):
    #Retrieve, update or delete a Lesson_Tag instance.
    def get_all_lesson_tags(self, lesson_id):
        try:
            return Lesson_Tag.objects.filter(lesson_id_number=lesson_id)
        except:
            raise Http404

    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        all_course_lessons = Lesson.objects.all().filter(course_id=course_id).values()
        course_json_response={}
        for lesson_obj in all_course_lessons:
            lesson_x_tag = self.get_all_lesson_tags(lesson_obj["id"])
            json_response=[]
            for tag in lesson_x_tag.values():
                tag_query=Tag.objects.filter(id=tag["tag_id_number"])
                tag_object={
                    "id":tag["id"],
                    "tag_name":tag_query.values()[0]["tag_name"],
                    "tag_id_number":tag["tag_id_number"]
                }
                json_response.append(tag_object)
            course_json_response[lesson_obj["id"]]=json_response

        return Response(course_json_response)

class SpecificCourseLanguagesView(APIView):
    """
    Retrieve, update or delete a Course_Tag instance.
    """
    def get_all_course_langs(self, course_id):
        try:
            return CourseLanguage.objects.filter(course_id=course_id)
        except:
            raise Http404

    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        course_languages = self.get_all_course_langs(course_id)
        return Response(course_languages.values())

class SpecificCourseLanguagesFilesView(APIView):
    """
    Retrieve, update or delete a Course_Tag instance.
    """
    def get_all_course_lang_files(self, course_id,language):
        try:
            language_sec = "."+language+"."
            return File.objects.filter(course_id=course_id).filter(file_name__contains=language_sec)
        except:
            raise Http404

    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        language = request.GET.get('language')
        files_languages = self.get_all_course_lang_files(course_id, language)
        return Response(files_languages.values())

class SpecificCourseFilesView(APIView):
    """
    Retrieve all course files
    """
    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        all_files = File.objects.filter(course_id=course_id)
        return Response(all_files.values())

class SpecificLessonFilesView(APIView):
    """
    Retrieve all lesson files
    """
    def get(self, request, format=None):
        lesson_id = request.GET.get('lesson_id')
        all_files = File.objects.filter(lesson_id=lesson_id)
        return Response(all_files.values())

class SpecificCourseTreeView(APIView):
    """
    Retrieve, update or delete a Course_Tag instance.
    """

    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        all_files = File.objects.filter(course_id=course_id)
        json_directory_wrap = {}
        json_directory = []
        for file in all_files:
            serializer = FileSerializer(file)
            file_course_location_text = serializer.data["file_course_location"]
            file_course_location = file_course_location_text.split(">>>")
            current_directory_level = 0
            json_directory = directory_recursive_generator(json_directory=json_directory, file_object=serializer.data, directory_path=file_course_location, current_directory_level=current_directory_level)
            json_directory_wrap = {"directory":json_directory}
        return Response(json_directory_wrap)

class SpecificLessonTreeView(APIView):
    """
    Retrieve
    """

    def get(self, request, format=None):
        lesson_id = request.GET.get('lesson_id')
        all_files = File.objects.filter(lesson_id=lesson_id)
        json_directory_wrap = {}
        json_directory = []
        for file in all_files:
            serializer = FileSerializer(file)
            file_course_location_text = serializer.data["file_course_location"]
            file_course_location = file_course_location_text.split(">>>")
            current_directory_level = 0
            json_directory = directory_recursive_generator(json_directory=json_directory, file_object=serializer.data, directory_path=file_course_location, current_directory_level=current_directory_level)
            json_directory_wrap = {"directory":json_directory}
        return Response(json_directory_wrap)

class CourseDirectoryTreeDetail(APIView):
    """
    Retrieve, update or delete the complete directory of files
    """
    def get(self, request, format=None):
        all_files = File.objects.all()
        json_directory_wrap = {}
        json_directory = []
        for file in all_files:
            serializer = FileSerializer(file)
            file_course_location_text = serializer.data["file_course_location"]
            file_course_location = file_course_location_text.split(">>>")
            current_directory_level = 0
            json_directory = directory_recursive_generator(json_directory=json_directory, file_object=serializer.data, directory_path=file_course_location, current_directory_level=current_directory_level)
            json_directory_wrap = {"directory":json_directory}
        return Response(json_directory_wrap)

class CourseLessonsDetail(APIView):
    """
    Retrieve, update or delete the complete directory of files
    """
    def get(self, request, format=None):
        course_id = request.GET.get('course_id')
        all_course_lessons = Lesson.objects.all().filter(course_id=course_id).values()
        return Response(all_course_lessons.values())

class SetNextLessonDetail(APIView):
    def get(self, request, format=None):
        lesson_id = request.GET.get('lesson_id')
        next_lesson_id = request.GET.get('next_lesson_id')
        first_lesson = Lesson.objects.get(pk=lesson_id)
        serialized_lesson_data = LessonSerializer(first_lesson).data
        lesson_new_next = {}
        lesson_new_next["next_lesson_id"] = next_lesson_id
        lesson_new_next["lesson_name"] = serialized_lesson_data["lesson_name"]
        lesson_new_next["lesson_identifier"] = serialized_lesson_data["lesson_identifier"]
        lesson_new_next["course_id"] = serialized_lesson_data["course_id"]
        serializer = LessonSerializer(first_lesson, data=lesson_new_next)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class Lesson_TagViewSet(viewsets.ModelViewSet):
    queryset = Lesson_Tag.objects.all()
    serializer_class = Lesson_TagSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseLanguageViewSet(viewsets.ModelViewSet):
    queryset = CourseLanguage.objects.all()
    serializer_class = CourseLanguageSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
