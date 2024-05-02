from django.urls import path
from .views import IndexView, CourseCreateView, LessonCreateView, LessonDetailView

app_name = 'materials'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('course/', CourseCreateView.as_view(), name='course'),
    path('courses/<int:course_id>/lessons/create/',
         LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    # Другие URL-шаблоны
]
