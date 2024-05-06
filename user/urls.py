from django.urls import path
from user.views import UserActivateView, UserCreateView, UserDetailView, UserUpdateView, login_view

app_name = 'user'

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('activate/<uidb64>/<token>/',
         UserActivateView.as_view(), name='activate_user'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('login/', login_view, name='login')

]
