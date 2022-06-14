from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('authapp:login')


class CustomLogoutView(LogoutView):
    template_name = 'mainapp/index.html'


class EditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])

