from utils.course_download_threader import course_download_thread_generator

#Run this file in the terminal, you will be prompted to input the information needed

user = raw_input("Coursera user: ")
password = raw_input("Coursera password: ")
course_name = raw_input("Course name: ")
thread_number = 1
course_download_thread_generator(user, password, course_name, thread_number)
