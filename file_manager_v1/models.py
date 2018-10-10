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
    #The course the file
    course_id = models.IntegerField()
    #The lesson the file is associated with
    lesson_id = models.IntegerField()

# Create your models here.
class Tag(models.Model):
    #Original file name found in cursera (Can be modified?)
    tag_name = models.CharField(max_length=100, unique=True)
    #Original file name found in cursera (Can be modified?)
    tag_importance = models.IntegerField()


# Create your models here.
class Lesson_Tag(models.Model):
    #Original file name found in cursera (Can be modified?)
    lesson_id_number = models.IntegerField()
    #The files location within a course, works like a directory
    tag_id_number = models.IntegerField()
    class Meta:
        unique_together = ("lesson_id_number", "tag_id_number")


# Create your models here.
class CourseLanguage(models.Model):
    #Original file name found in cursera (Can be modified?)
    course_id = models.IntegerField()
    #The files location within a course, works like a directory
    language = models.CharField(max_length=100)
    class Meta:
        unique_together = (("course_id", "language"),)


#File group
class Lesson(models.Model):
    #The name of the lesson
    lesson_name = models.CharField(max_length=500)
    #Lesson String identifier
    lesson_identifier = models.CharField(max_length=500)
    #In a ordered list each lesson has a successor. The last object has a next_lesson=0
    next_lesson_id = models.IntegerField()
    #The course the lesson is associated to
    course_id = models.IntegerField()
