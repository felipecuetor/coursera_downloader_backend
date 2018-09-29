import threading
import time
import sys
from os import listdir
import datetime
from courseradl.coursera.courseradl import simple_course_download
from utils.file_manager_utils import course_static_directory_analyzer_remote
from utils.file_manager_utils import course_element_generator

# A basic threading algorithm that creates a course download thread
def course_download_thread_generator(user, password, course_name, thread_number):
	print("Preparing download...")

	if thread_number is None:
		thread_number = 1;

	class myThread (threading.Thread):

		def __init__(self, user_thread, password_thread, course_name_thread):
			threading.Thread.__init__(self)
			self.user_thread = user_thread
			self.password_thread = password_thread
			self.course_name_thread = course_name_thread
		def run(self):
			path="./data/"+self.course_name_thread
			simple_course_download(self.user_thread, self.password_thread ,self.course_name_thread, "./data/")
			#course_static_directory_analyzer_remote(path)
			#course_element_generator(self.course_name_thread, datetime.datetime.now(), False, False, False)
			#zip_course(path)

	# Create new threads
	threads = []
	for x in range(0, thread_number):
		thread = myThread(user, password, course_name)
		# Start new Threads
		thread.start()
		# Add threads to thread list
		threads.append(thread)

	# Wait for all threads to complete
	#for t in threads:
	#	t.join()
