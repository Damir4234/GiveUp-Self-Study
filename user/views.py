from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from user.models import User


class UserCreateView(CreateView):
    model = User
    fields = ('email', 'password',)
    success_url = reverse_lazy('materials:home')
