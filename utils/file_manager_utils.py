import os

def get_array_keys(array):
    keys = []
    for element in array:
        for key, value in element.iteritems():
            keys.append(key)
    return keys

def directory_recursive_generator(json_directory, file_object, directory_path, current_directory_level):
    current_directory_name =directory_path[current_directory_level]
    json_directory_resp = json_directory
    if((current_directory_level+1)==len(directory_path)):
        json_directory_resp.append({current_directory_name:file_object["id"]})
        #print "File detected "+str(current_directory_name)+" "+str(current_directory_level)
        return json_directory_resp
    else:
        add_new_directory = True
        temp_dict = {}
        #print "Searching for folder "+str(current_directory_name)+" "+str(current_directory_level)
        for idx, json_directory_object in enumerate(json_directory):
            for attribute, value in json_directory_object.iteritems():

                if(attribute==current_directory_name):
                    #print "Existing folder detected "+str(current_directory_name)+" "+str(current_directory_level)
                    add_new_directory = False
                    append_object = {current_directory_name:directory_recursive_generator(value, file_object, directory_path, current_directory_level+1)}
                    value_added=value+append_object[attribute]

                    temp_dict[attribute] = value_added
                    #json_directory_object[attribute] = value
                    #json_directory_resp[idx] = json_directory_object
        if add_new_directory:
            #print "New folder detected "+str(current_directory_name)+" "+str(current_directory_level)
            json_directory_resp.append({current_directory_name:directory_recursive_generator([], file_object, directory_path, current_directory_level+1)})
        #print temp_dict

    return json_directory_resp

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

def detect_language_in_name(text, course_id):
    period_split = text.split(".")
    if(len(period_split)==3):
        url = 'http://localhost:8000/courselanguage/'
        payload = {
            'course_id': course_id,
            'language': period_split[1]
        }
        #print file_namer
        r = requests.post(url, data=payload)
