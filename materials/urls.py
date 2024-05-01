from django.urls import path
from .views import IndexView, CourseCreateView, LessonCreateView

app_name = 'materials'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('course/', CourseCreateView.as_view(), name='course'),
    path('courses/<int:course_id>/lessons/create/',
         LessonCreateView.as_view(), name='lesson_create'),
    # Другие URL-шаблоны
]
