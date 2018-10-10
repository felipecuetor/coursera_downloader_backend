import os
import requests
import datetime
import json

#Allows you to manually execute the data generation algorithm that analyzes all courses within the data folder in the root of the directory.
#This algorithm recursivly goes deeper and deeper within the folder system searching for the files.

def course_static_directory_analyzer_remote(course_path, recursize_directory_path, recursive_location_path, course_id, existing_lessons, existing_lessons_files ):
    course_directory = os.listdir(course_path)
    existing_lessons_in_directory={}
    existing_lessons_in_directory_files={}
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
            existing_lessons = course_static_directory_analyzer_remote(dir2+"/", recursize_directory_path+">>>"+str(element), recursive_location_path+">>>"+folder_name_division, course_id, existing_lessons, existing_lessons_files)
        else:
            file_name_division=""
            file_name=""
            split1 = element.split("_")
            if split1[0].replace('.','',1).isdigit():
                file_name_division=split1[0]+">>>"+element[3:]
                file_name=element[2:]
                lesson_name=element[3:]
                lesson_identifier=split1[0]
            else:
                file_name_division=element
                file_name=element
                lesson_name=file_name_division
                lesson_identifier=file_name
            file_name = element
            file_directory_path = recursize_directory_path+">>>"+str(element)
            file_location_path = recursive_location_path+">>>"+file_name_division
            #url = 'http://localhost:8080/files/'
            payload = {
                'file_name': file_name,
                'file_course_location': file_location_path,
                'file_directory': file_directory_path,
                'course_id':course_id
            }
            #r = requests.post(url, data=payload)

            if lesson_identifier not in existing_lessons_in_directory:
                existing_lessons_in_directory_files[lesson_identifier]=[]
            existing_lessons_in_directory_files[lesson_identifier].append(payload)
            existing_lessons_in_directory[lesson_identifier]={"lesson_name":lesson_name,"lesson_identifier":lesson_identifier}
    existing_lessons.append(existing_lessons_in_directory)
    existing_lessons_files.append(existing_lessons_in_directory_files)
    return existing_lessons


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

def dump_file_list(file_list, course_id, lesson_id):
    for file in file_list:
        url = 'http://localhost:8080/files/'
        payload = file
        payload["lesson_id"] = lesson_id
        print payload
        r = requests.post(url, data=payload)

def dump_lesson_list(existing_lessons,course_id, existing_lessons_files):
    current_list = list(reversed(existing_lessons))
    directory_lesson_file_list = list(reversed(existing_lessons_files))
    previous_element_id = 0
    for id, current in enumerate(current_list):
        existing_lessons_in_directory_keys=list(reversed(current.keys()))
        lesson_file_list = directory_lesson_file_list[id]
        for key in existing_lessons_in_directory_keys:
            current_lesson = current[key]
            current_lesson_file_list = lesson_file_list[key]
            url = 'http://localhost:8080/lesson/'
            payload = current_lesson
            payload["course_id"]=course_id
            payload["next_lesson_id"]=previous_element_id
            r = requests.post(url, data=payload)
            previous_element = json.loads(r.content)
            previous_element_id = previous_element["id"]
            dump_file_list(current_lesson_file_list, course_id, previous_element_id)

dir1 = "./data/"
course_directory = os.listdir(dir1)

for element in course_directory:
    dir2 = dir1+str(element)
    existing_lessons=[]
    existing_lessons_files=[]
    if os.path.isdir(dir2):
        print("Course post")
        course_info = json.loads(course_element_generator(element, datetime.datetime.now(), False, False, False))
        print("File post")
        lessons_files_tuple = course_static_directory_analyzer_remote(dir2+"/", element, element, course_info["id"],existing_lessons,existing_lessons_files)
        print("Lesson post")
        dump_lesson_list(existing_lessons,course_info["id"],existing_lessons_files)
        print("language post")
        find_course_languages(course_info)
