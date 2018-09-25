import os
import requests
import datetime
import json

#Allows you to manually execute the data generation algorithm that analyzes all courses within the data folder in the root of the directory.
#This algorithm recursivly goes deeper and deeper within the folder system searching for the files.

def course_static_directory_analyzer_remote(course_path, recursize_directory_path, recursive_location_path, course_id ):
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
            course_static_directory_analyzer_remote(dir2+"/", recursize_directory_path+">>>"+str(element), recursive_location_path+">>>"+folder_name_division, course_id)
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
            url = 'http://localhost:8080/files/'
            payload = {
                'file_name': file_name,
                'file_course_location': file_location_path,
                'file_directory': file_directory_path,
                'course_id':course_id
            }
            r = requests.post(url, data=payload)
            print r.content


def course_element_generator(course_name, course_download_date, course_revised, course_download_available, course_error):
    url = 'http://localhost:8080/courses/'
    payload = {
        'course_name': course_name,
        'course_download_date': course_download_date,
        'course_revised': course_revised,
        'course_download_available':course_download_available,
        'course_error':course_error
    }
    r = requests.post(url, data=payload)
    print r.content
    return r.content

def detect_language_in_name(text, course_id):
    period_split = text.split(".")
    if(len(period_split)==3):
        url = 'http://localhost:8080/courselanguage/'
        payload = {
            'course_id': course_id,
            'language': period_split[1]
        }
        r = requests.post(url, data=payload)
        print r.content

def find_course_languages(course_info):
    url = 'http://localhost:8080/course_files/?course_id='+str(course_info["id"])
    print(url)
    r = requests.get(url)
    course_files = r.content
    for file in json.loads(course_files):
        detect_language_in_name(file["file_name"], course_info["id"])

dir1 = "./data/"
course_directory = os.listdir(dir1)

for element in course_directory:
    dir2 = dir1+str(element)
    if os.path.isdir(dir2):
        print("Course post")
        course_info = json.loads(course_element_generator(element, datetime.datetime.now(), False, False, False))
        print("File post")
        course_static_directory_analyzer_remote(dir2+"/", element, element, course_info["id"])
        print("language post")
        find_course_languages(course_info)
