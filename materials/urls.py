from django.urls import path
from .views import IndexView

app_name = 'materials'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    # Другие URL-шаблоны
]
