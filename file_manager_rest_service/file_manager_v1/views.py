# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from file_manager_v1.models import File, Tag, CourseXTag
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from file_manager_v1.serializers import UserSerializer, GroupSerializer, FileSerializer, TagSerializer, CourseXTagSerializer
from file_manager_utils import directory_recursive_generator
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
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class CourseXTagViewSet(viewsets.ModelViewSet):
    queryset = CourseXTag.objects.all()
    serializer_class = CourseXTagSerializer
