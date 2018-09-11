import os
from coursera import coursera_dl

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

def course_static_directory_analyzer(course_path, recursize_directory_path, recursive_location_path ):
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
            course_static_directory_analyzer(dir2+"/", recursize_directory_path+">>>"+str(element), recursive_location_path+">>>"+folder_name_division)
        elif os.path.isfile(dir2):
            file_name_division=""
            file_name=""
            split1 = element.split("_")
            if split1[0].replace('.','',1).isdigit():
                file_name_division=split1[0]+">>>"+element[3:]
                file_name=element[2:]
            else:
                file_name_division=element
                file_name=element

def download_course():
    course_name = raw_input("Course name: ")
    user = raw_input("Coursera user: ")
    password = raw_input("Coursera password: ")
