# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class File(models.Model):
    file_name = models.CharField(max_length=1000)
    file_directory = models.CharField(max_length=1000)
