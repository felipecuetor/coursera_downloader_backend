import os
from coursera import coursera_dl

def directory_recursive_generator(json_directory, file_object, directory_path, current_directory_level):
    print "Before: "+str(current_directory_level)
    print json_directory
    json_directory_resp = json_directory
    current_directory_name =directory_path[current_directory_level]
    if((current_directory_level+1)==len(directory_path)):
        json_directory_resp.append({current_directory_name:file_object["file_directory"]})
    else:
        for idx, json_directory_object in enumerate(json_directory):
            for attribute, value in json_directory_object.iteritems():
                if(attribute==current_directory_name):
                    append_object = {current_directory_name:directory_recursive_generator([], file_object, directory_path, current_directory_level+1)}
                    value.append(append_object)
                    json_directory_object[attribute] = value
                    json_directory_resp[idx] = json_directory_object
                    print "After: "+str(current_directory_level)
                    print json_directory_resp
                    return json_directory_resp
        json_directory_resp.append({current_directory_name:directory_recursive_generator([], file_object, directory_path, current_directory_level+1)})
    print "After: "+str(current_directory_level)
    print json_directory_resp

    return json_directory_resp

def download_course():
    course_name = raw_input("Course name: ")
    user = raw_input("Coursera user: ")
    password = raw_input("Coursera password: ")
    print(dir(coursera_dl))
