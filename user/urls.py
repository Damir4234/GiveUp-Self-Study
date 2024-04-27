from django.urls import path
from user.views import UserActivateView, UserCreateView

app_name = 'user'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('activate/<uidb64>/<token>/',
         UserActivateView.as_view(), name='activate_user'),
    # Другие URL-шаблоны
]
