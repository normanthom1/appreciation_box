from django.contrib.auth import models
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from . models import Post
from django.contrib.auth.decorators import login_required
import datetime
import random
# from .quotes import quotes
# Create your views here.

def filter_posts():
    date = datetime.date.today()
    startweek = date - datetime.timedelta(date.weekday())
    endweek = startweek + datetime.timedelta(7)
    posts = Post.objects.filter(created_at__range=[startweek, endweek]).order_by('-created_at')
    return posts

quotes = [
    ("JFK", "As we express our gratitude, we must never forget that the "
            "highest appreciation is not to utter words, but to live by them."),
    ("Ralph Waldo Emerson", "You cannot do a kindness too soon because you "
                            "never know how soon it will be too late."),
    ("Robert Holden", "The real gift of gratitude is that the more grateful "
                      "you are, the more present you become."),
    ("Kristin Armstrong", "When we focus on our gratitude, the tide of disappointment "
                          "goes out and the tide of love rushes in.")
]

def generate_random_quote():
    num = random.randint(0, 3)
    author = quotes[num][0]
    quote = quotes[num][1]
    return author, quote

@login_required(login_url='login')
def home(request):
    posts = filter_posts()
    author, quote = generate_random_quote()
    context = {
        'posts': posts,
        'author': author,
        'quote': quote,
    }

    return render(request, 'base.html', context)


def add_post(request):
    # posts = Post.objects.filter(user=request.user).order_by('-created_at')
    posts = filter_posts()
    if request.method == "POST":
        post = request.POST['post']
        post = Post.objects.create(
            post=post,
            user=request.user
        )
        post.save()
        context = {
            'posts': posts
        }
    return render(request, 'components/posts.html', context)


def delete_todo(request, id):
    todo = Post.objects.get(pk=id)
    print(todo)
    todo.delete()
    # posts = Post.objects.filter(user=request.user).order_by('-created_at')
    posts = filter_posts()
    return render(request, 'components/posts.html', {'posts': posts})


def mark_complete(request, id):
    post = Post.objects.get(pk=id)
    print(post)
    if request.method == "POST":
        if Post.post_status == False:
            post.post_status = True
        else:
            post.post_status = False
    post.save()
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'components/posts.html', {'posts': posts})


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email already registered')
                    return redirect('register')

                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password,
                    )

                    # user.is_active = False
                    user.save()
                    return redirect('login')
        else:
            messages.warning(request, "Password don't Match")
            return redirect('register')

    author, quote = generate_random_quote()
    context = {
        'author': author,
        'quote': quote
    }

    return render(request, 'components/register.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('login')

    author, quote = generate_random_quote()
    context = {
        'author': author,
        'quote': quote
    }

    return render(request, 'components/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('login')


def check_user(request):
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            return HttpResponse('<span id = "username-check" class="warning-text font-weight-bold lead small text-danger px-2">Username already exists.</span')
        else:
            return HttpResponse('<span id = "username-check" class="warning-text lead small font-weight-bold text-danger px-2">Username available.</span')


def email_check(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return HttpResponse('<span id = "email-check" class="warning-text font-weight-bold lead small text-danger px-2">Email already exists.</span')
        else:
            return HttpResponse('<span id = "email-check" class="warning-text font-weight-bold lead small text-danger px-2">Email Not registered</span')
