from django.urls import path
from .views import CourseDetailView, CourseListView, IndexView, CourseCreateView, LessonCreateView, LessonDetailView, LessonListView

app_name = 'materials'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('course/create/', CourseCreateView.as_view(), name='course'),
    path('courses/<int:course_id>/lessons/create/',
         LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:course_id>/lessons/',
         LessonListView.as_view(), name='lesson_list'),
    # Другие URL-шаблоны
]
