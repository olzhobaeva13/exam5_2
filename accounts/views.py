from django.shortcuts import render
from django.shortcuts import render

from django.shortcuts import render, redirect, reverse
from django.views import View
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse

User = get_user_model()


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('posts_list_url'))
        form = LoginForm()
        return render(request, 'accounts/login.html', context={'form': form})

    def post(self, request):
        bound_form = LoginForm(request.POST)
        if bound_form.is_valid():
            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('posts_list_url'))
        return render(request, 'accounts/login.html', context={'form': bound_form})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('posts_list_url'))
        register_form = RegisterForm
        return render(request, 'accounts/register.html', context={'register_form': register_form})

    def post(self, request):
        bound_form = LoginForm(request.POST)
        if bound_form.is_valid():
            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect(reverse('post_create_url'))

        return render(request, 'accounts/register.html', context={'register_form': bound_form})


def logout_view(request):
    logout(request)
    return redirect(reverse('login_url'))

