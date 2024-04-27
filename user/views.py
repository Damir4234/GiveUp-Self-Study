
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from user.models import User
from django.shortcuts import render, redirect


class UserCreateView(CreateView):
    model = User
    fields = ('email', 'password',)
    success_url = reverse_lazy('materials:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Устанавливаем is_active в False
        user.save()

        # Отправляем электронное письмо с ссылкой для активации учетной записи
        self.send_activation_email(user)

        return super().form_valid(form)

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Активация учетной записи'

    # Генерируем токен и кодируем UID для активации учетной записи
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

    # Передаем uid и token в контекст шаблона
        message = render_to_string('user/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uidb64': uid,
            'token': token,
        })
        send_mail(mail_subject, message, 'w4atifif@yandex.ru', [user.email])


class UserActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('materials:home')
        else:
            raise Http404
