
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


class UserCreateView(CreateView):
    model = User
    fields = ('email', 'password',)
    success_url = reverse_lazy('materials:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()

        self.send_activation_email(user)

        return super().form_valid(form)

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Активация учетной записи'

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

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


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            return redirect('materials:dashboard')
        else:

            messages.error(
                request, 'Неверный адрес электронной почты или пароль.')
            return render(request, 'user/login.html')

    return render(request, 'user/login.html')


class UserDetailView(DetailView):
    model = User

    def get_object(self):

        user = get_object_or_404(User, pk=self.kwargs['pk'])

        print("User detail:", user)
        return user


class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'user/user_update_form.html'

    def get_success_url(self):
        return reverse_lazy('user:profile', kwargs={'pk': self.object.pk})
