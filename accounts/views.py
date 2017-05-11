# -*- coding: utf-8 -*-


from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate,get_user_model,login,logout
from .forms import UserLoginForm, UserRegisterForm
from .models import User, Follow
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request,"form.html",{"form": form})


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request,new_user)
        return redirect("/")
    context = {
        "form": form
    }
    return render(request,"form.html",context)


def logout_view(request):
    logout(request)
    return redirect("/")
    return render(request,"form.html",{})


def followlist_view(request):
    if not request.user.is_authenticated:
        raise Http404
    users = User.objects.filter(~Q(id = request.user.id )).filter(~Q(id=1))
    followed_users =  User.objects.all().filter(following__follower__email=request.user.email)
    users = set(users) - set(followed_users)
    print (users)
    return render(request,"followlist.html",{"users":users,"followed_users":followed_users})


def unfollow_view(request,id=None):
    if not request.user.is_authenticated:
        raise Http404

    Follow.objects.all().filter(follower=request.user,following=User.objects.get(id=id)).delete()
    return redirect('/follow')


def follow_view(request,id=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = Follow()
    instance.following = User.objects.get(id=id)
    instance.follower = request.user
    instance.save()
    return redirect('/follow')


@login_required(login_url='/login/')
def profile_view(request,id=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = User.objects.get(id=id)
    return render(request, "profile.html", {"user":instance})


def search_view(request):
    if not request.user.is_authenticated:
        raise Http404
    query = request.GET.get("q")
    if query:
        userlist = User.objects.all().filter(Q(name__icontains=query)
                                             | Q(username__icontains=query))
    return render(request,"search.html",{"users":userlist})

