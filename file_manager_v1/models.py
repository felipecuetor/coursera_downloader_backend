# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
    #Original course name
    course_name = models.CharField(max_length=1000, unique=True)
    course_download_date = models.CharField(max_length=1000, unique=True)
    course_revised = models.BooleanField(default=False, unique=True)

# Create your models here.
class File(models.Model):
    #Original file name found in cursera (Can be modified?)
    file_name = models.CharField(max_length=1000, unique=True)
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
class CourseXTag(models.Model):
    #Original file name found in cursera (Can be modified?)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    #The files location within a course, works like a directory
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
