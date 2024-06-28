"""
URL configuration for booklet_repository project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from booklets import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup', views.CustomSignupView.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.booklet_list, name='signup'),
    path('booklets/', views.booklet_list, name='booklet_list'),
    path('upload/', views.upload_booklet, name='upload_booklet'),
    path('delete/<int:booklet_id>/', views.delete_booklet, name='delete_booklet'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
