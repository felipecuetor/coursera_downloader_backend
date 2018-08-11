# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from quickstart.models import File
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from quickstart.serializers import UserSerializer, GroupSerializer
from file_manager_utils import move_file, get_file_structure

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, format=None):
        return get_file_structure(request)

    def post(self, request, format=None):
        return move_file(request)
