import os
import requests
import datetime

#Allows you to manually execute the data generation algorithm that analyzes all courses within the data folder in the root of the directory.
#This algorithm recursivly goes deeper and deeper within the folder system searching for the files.

def course_static_directory_analyzer_remote(course_path, recursize_directory_path, recursive_location_path ):
    course_directory = os.listdir(course_path)
    for element in course_directory:
        element=str(element)
        dir2 = course_path+str(element)
        if os.path.isdir(dir2):
            folder_name_division=""
            split1 = element.split("_")
            if split1[0].replace('.','',1).isdigit():
                folder_name_division=split1[0]+">>>"+element[3:]
            else:
                folder_name_division=element
            course_static_directory_analyzer_remote(dir2+"/", recursize_directory_path+">>>"+str(element), recursive_location_path+">>>"+folder_name_division)
        else:
            file_name_division=""
            file_name=""
            split1 = element.split("_")
            if split1[0].replace('.','',1).isdigit():
                file_name_division=split1[0]+">>>"+element[3:]
                file_name=element[2:]
            else:
                file_name_division=element
                file_name=element
            file_name = element
            file_directory_path = recursize_directory_path+">>>"+str(element)
            file_location_path = recursive_location_path+">>>"+file_name_division
            url = 'http://localhost:8000/files/'
            payload = {
            'file_name': file_name,
            'file_course_location': file_location_path,
            'file_directory': file_directory_path
            }
            #print file_namer
            r = requests.post(url, data=payload)


def course_element_generator(course_name, course_download_date, course_revised, course_download_available, course_error):
    url = 'http://localhost:8000/courses/'
    payload = {
        'course_name': course_name,
        'course_download_date': course_download_date,
        'course_revised': course_revised,
        'course_download_available':course_download_available,
        'course_error':course_error
    }
    #print file_namer
    r = requests.post(url, data=payload)

dir1 = "./data/"
course_directory = os.listdir(dir1)

for element in course_directory:
    dir2 = dir1+str(element)
    if os.path.isdir(dir2):
        #print dir2
        course_static_directory_analyzer_remote(dir2+"/", element, element)
        course_element_generator(element, datetime.datetime.now(), False, False, False)
