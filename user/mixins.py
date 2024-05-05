from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


class LoginRequiredMixin(AccessMixin):
    """Миксин, который требует аутентификации пользователя."""

    # Путь для перенаправления пользователя на страницу входа
    login_url = reverse_lazy('user:login')

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            # Если пользователь не аутентифицирован, перенаправляем его на страницу входа
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
