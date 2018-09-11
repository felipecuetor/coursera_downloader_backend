import os
import requests

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


dir1 = "./data/"
course_directory = os.listdir(dir1)

for element in course_directory:
    dir2 = dir1+str(element)
    if os.path.isdir(dir2):
        #print dir2
        course_static_directory_analyzer_remote(dir2+"/", element, element)
