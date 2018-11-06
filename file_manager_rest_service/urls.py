"""file_manager_rest_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from file_manager_v1 import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'files', views.FileViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'lesson_x_tag', views.Lesson_TagViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'courselanguage', views.CourseLanguageViewSet)
router.register(r'lesson', views.LessonViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^file_detail/(?P<pk>[0-9]+)/$', views.FileDetail.as_view()),
    url(r'^move_file/(?P<pk>[0-9]+)/$', views.MoveFileView.as_view()),
    url(r'^directory_tree/', views.CourseDirectoryTreeDetail.as_view()),
    url(r'^download_course/', views.downloadCourse),
    url(r'^lesson_tags/', views.SpecificLessonTagsView.as_view()),
    url(r'^course_languages/', views.SpecificCourseLanguagesView.as_view()),
    url(r'^course_files/', views.SpecificCourseFilesView.as_view()),
    url(r'^course_lang_files/', views.SpecificCourseLanguagesFilesView.as_view()),
    url(r'^course_directory_tree/', views.SpecificCourseTreeView.as_view()),
    url(r'^lesson_directory_tree/', views.SpecificLessonTreeView.as_view()),
    url(r'^course_lessons/', views.CourseLessonsDetail.as_view()),
    url(r'^set_next_lesson/', views.SetNextLessonDetail.as_view()),
    url(r'^lesson_files/', views.SpecificLessonFilesView.as_view()),
    url(r'^course_toggle_revised/', views.SpecificCourseToggleRevised.as_view()),
    url(r'^course_tags/', views.LessonListTagsView.as_view()),
    url(r'^download_course_language_contents/', views.DownloadCourseLanguageContents.as_view()),
]
