from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Script, DataFragment
from .forms import UCForm
import random


@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        user_explanation = request.POST.get('script_translation')
        script_id = request.POST.get('script_id')
        script_ = Script.objects.get(id=int(script_id))
        df = DataFragment(script=script_, explanation=user_explanation, user=request.user)
        df.save()

    scripts_number = len(Script.objects.all())
    script_to_show = Script.objects.all()[random.randint(0, scripts_number - 1)]
    context = {
        'script': script_to_show,
    }

    return render(request, 'landingapp/index.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UCForm()

    if request.method == 'POST':
        form = UCForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Аккаунт для ' + username + ' успешно создан!')
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'landingapp/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')

        user = authenticate(request, username=username_, password=password_)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Неправильное имя пользователья или пароль')
    context = {}
    return render(request, 'landingapp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
