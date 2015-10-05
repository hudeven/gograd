from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, ResearcherProfile
from .forms import PostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
import re 
from django.db.models import Q

#For cayley
import requests
import sys
from django.contrib.staticfiles import finders
# Create your views here.

def search(request):
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(position__icontains=query)
        )   
        results = ResearcherProfile.objects.filter(qset).distinct()
    else:
        results = []
    form = SearchForm()
    return render(request, 'blog/search.html', {'profiles':results, 'form':form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def researcher_profile_list(request):
    form = SearchForm()
    researcherProfiles = ResearcherProfile.objects.filter()
    return render(request, 'blog/profile_list.html', {'profiles': researcherProfiles, 'form' : form})

def researcher_detail(request, pk):
    profile = get_object_or_404(ResearcherProfile, pk=pk)
    return render(request, 'blog/researcher_detail.html',{'profile':profile})

def test(request):
    return render(request, 'blog/test.html')

def searchStaticFiles(request):
    result = finders.find('css/blog.css') 
    return render(request, 'blog/searchStaticFiles.html', {'results':result})

#only 10 vertex randomly
def cayley_show_all_vertex(request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "g.V().GetLimit(10)" 
    response = requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    return render(request, 'blog/cayley_response.html', {'response':response}) 

def cayley_detail(request, tmpID):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "g.V(\"%s\").Both(\"coauthor\").Both(\"realname\").All()" % tmpID 
    response1 = requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    data = "g.V(\"%s\").Both(\"realname\").All()" % tmpID 
    response2= requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    return render(request, 'blog/cayley_response.html', {'coauthor':response1, 'realname':response2}) 

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post':post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post) 
    return render(request, 'blog/post_edit.html', {'form': form}) 

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm() 
    return render(request, 'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date') 
    return render(request, 'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish() 
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form}) 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('blog.views.post_list')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})
#only 10 vertex randomly
def cayley_show_all_vertex(request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "g.V().GetLimit(10)" 
    response = requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    return render(request, 'blog/cayley_response.html', {'response':response}) 

def cayley_detail(request, tmpID):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "g.V(\"%s\").Both(\"coauthor\").Both(\"realname\").All()" % tmpID 
    response1 = requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    data = "g.V(\"%s\").Both(\"realname\").All()" % tmpID 
    response2= requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    return render(request, 'blog/cayley_response.html', {'coauthor':response1, 'realname':response2}) 

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post':post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post) 
    return render(request, 'blog/post_edit.html', {'form': form}) 

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm() 
    return render(request, 'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date') 
    return render(request, 'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish() 
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form}) 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('blog.views.post_list')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})
def test(request):
    return render(request, 'blog/test.html')

#only 10 vertex randomly
def cayley_show_all_vertex(request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "g.V().GetLimit(10)" 
    response = requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    return render(request, 'blog/cayley_response.html', {'response':response}) 

def cayley_detail(request, tmpID):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "g.V(\"%s\").Both(\"coauthor\").Both(\"realname\").All()" % tmpID 
    response1 = requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    data = "g.V(\"%s\").Both(\"realname\").All()" % tmpID 
    response2= requests.post('http://127.0.0.1:64210/api/v1/query/gremlin', headers=headers, data=data)      
    return render(request, 'blog/cayley_response.html', {'coauthor':response1, 'realname':response2}) 

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post':post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post) 
    return render(request, 'blog/post_edit.html', {'form': form}) 

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm() 
    return render(request, 'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date') 
    return render(request, 'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish() 
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form}) 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('blog.views.post_list')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})
