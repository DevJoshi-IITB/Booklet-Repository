from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import SignUpForm, BookletUploadForm
from .models import Booklet
from allauth.account.views import SignupView
from django.urls import reverse

# Create your views here.   
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booklet_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('booklet_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def booklet_list(request):
    if request.user.is_superuser:
        booklets = Booklet.objects.filter(author=request.user)
    else:
        booklets = Booklet.objects.all()
    return render(request, 'booklet_list.html',{'booklets':booklets})

@login_required
def upload_booklet(request):
    if request.method == 'POST':
        form = BookletUploadForm(request.POST, request.FILES)
        if form.is_valid():
            booklet = form.save(commit=False)
            booklet.author = request.user
            booklet.save()
            return redirect('booklet_list')
    else:
        form = BookletUploadForm()
    return render(request, 'upload_booklet.html', {'form': form})   

@login_required
def delete_booklet(request, booklet_id):
    booklet = Booklet.objects.get(id=booklet_id)
    if request.user.is_superuser and booklet.author == request.user:
        booklet.delete()
    return redirect('booklet_list')

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CustomSignupView(SignupView):
    def get_success_url(self):
        return reverse('booklet_list')  

