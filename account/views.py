from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import LoginForm, UserRegisterForm,\
                   UserEditForm, ProfileEditForm


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            Profile.objects.create(user=user)
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return render(request, 'account/account_created.html', {'user': auth_user})
    form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authenticated \
                 Successfully.')
            else:
                return HttpResponse('Can\'t find account.')
        else:
            return HttpResponse('Invalid information supplied.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully.')
        else:
            messages.error(request, 'Something went missing!')
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit_profile.html', context)


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html', {'section': 'dashboard'})
