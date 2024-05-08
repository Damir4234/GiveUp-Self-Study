from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy


class LoginRequiredMixin(AccessMixin):
    """Миксин, который требует аутентификации пользователя."""

    login_url = reverse_lazy('user:login')

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
