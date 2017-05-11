# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post,Like
from accounts.models import User,Follow
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def post_list(request):
    if not request.user.is_authenticated:
        return redirect("login/")


    following_list = []
    for f in Follow.objects.all().filter(follower=request.user):
        following_list.append(f.following)
    following_list.append(request.user)
    queryset = Post.objects.all().filter(user__in=following_list)
    likes = Like.objects.all().filter()
    commentform = CommentForm()
    context = {
        "object_list": queryset,
        "likes": likes,
        "form":commentform
    }

    return render(request,"posts_list.html",context)


@login_required(login_url='/login/')
def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request,id= None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    context = {
        "instance": instance
    }
    return render(request, "post_detail.html", context)


def post_update(request,id=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance= instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,"successfully deleted")
    return redirect("posts:list")


def like_post(request,id=None):
    post = get_object_or_404(Post,id=id)
    like = Like.objects.get_or_create(user=request.user,post=post)
    likes = post.liked_post.count()
    return HttpResponse(likes)


def comment_view(request,id=None):
    post = Post.objects.get(id=id)
    for i in post.post_comments.all():
        print (i.user)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.post = post
        instance.save()
        print (instance.user)
        print (instance.content)
        return redirect("/")
    return redirect("/")

