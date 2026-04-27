from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User(
            email=form.cleaned_data['email'],
            name=form.cleaned_data['name'],
            role='student',
            is_verified=True,
        )
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, token):
    messages.info(request, 'Email verification is not required.')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].lower()
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, 'Invalid email or password.')
        elif not user.is_verified:
            messages.error(request, 'Your account is not verified.')
        elif user.is_blocked:
            messages.error(request, 'Your account is blocked due to an overdue book. Please return it to the library.')
        else:
            login(request, user)
            if user.is_admin:
                return redirect('librarian_dashboard')
            return redirect('book_list')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')