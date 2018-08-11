import os
from rest_framework.response import Response

def move_file(request):
    print request

def get_file_structure(request):
    print request
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print dir_path
    dir_list = os.listdir(dir_path)
    print dir_list
