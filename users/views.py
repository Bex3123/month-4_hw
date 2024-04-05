import random

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm, EditProfileForm, VerifyForm
from .models import UserProfile, SMSCodes


def register_view(request):
    if request.method == "GET":
        return render(request, 'users/register.html', {'form': RegisterForm()})
    elif request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            avatar = form.cleaned_data['avatar']
            bio = form.cleaned_data['bio']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False
            )
            UserProfile.objects.create(
                user=user,
                avatar=avatar,
                bio=bio
            )
            code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
            SMSCodes.objects.create(
                user=user,
                code=code
            )
            return redirect('verify', code=code)
        else:
            return render(request, 'users/register.html', {"form": form})


def verify_view(request, code):
    if request.method == 'GET':
        return render(request, 'users/verify.html', {'form': VerifyForm(), 'code': code})
    elif request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            if entered_code == code:
                if SMSCodes.objects.filter(code=code).exists():
                    sms_code = SMSCodes.objects.get(code=code)
                    sms_code.user.is_active = True
                    sms_code.user.save()
                    sms_code.delete()
                    return redirect('login')
                else:
                    form.add_error(None, "Invalid code")
            else:
                form.add_error('code', "Invalid code")
        return render(request, 'users/verify.html', {'form': form, 'code': code})


def login_view(request):
    if request.method == 'GET':
        context = {
            'form': LoginForm()
        }
        return render(request=request, template_name='users/login.html', context=context)
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error('username', 'Username or password is incorrect!')
        return render(request=request, template_name='users/login.html', context={"form": form})


def profile_view(request):
    if request.method == 'GET':
        return render(request, 'users/profile.html', {"user": request.user})


@login_required
def profile_update_view(request):
    if request.method == 'GET':
        profile = UserProfile.objects.get(user=request.user)
        form = EditProfileForm(instance=profile)
        return render(request, 'users/profile_update.html', {'form': form})
    elif request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
        else:
            return render(request, 'users/profile_update.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/products/')
