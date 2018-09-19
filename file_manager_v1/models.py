# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
    #Original course identafier name
    course_name = models.CharField(max_length=1000, unique=True)
    #When was the course downloaded
    course_download_date = models.CharField(max_length=1000)
    #Has the course been revised by a student
    course_revised = models.BooleanField(default=False)
    #Is the course available as a zip file for download
    course_download_available = models.BooleanField(default=False)
    #Is the course available as a zip file for download
    course_error = models.BooleanField(default=False)

# This file system does not allow for folders to be created.
# Files can be grouped together by giving them the same file_course_location up to the file name
class File(models.Model):
    #Original file name found in cursera (Can be modified?)
    file_name = models.CharField(max_length=1000)
    #The files location within a course, works like a directory
    file_course_location = models.CharField(max_length=1000, default="", unique=True)
    #The real location the file can be found within the course location (Its a relative directory)
    file_directory = models.CharField(max_length=1000, unique=True)

# Create your models here.
class Tag(models.Model):
    #Original file name found in cursera (Can be modified?)
    tag_name = models.CharField(max_length=100, unique=True)
    #Original file name found in cursera (Can be modified?)
    tag_importance = models.IntegerField()


# Create your models here.
class Course_Tag(models.Model):
    #Original file name found in cursera (Can be modified?)
    course_id_number = models.IntegerField()
    #The files location within a course, works like a directory
    tag_id_number = models.IntegerField()
