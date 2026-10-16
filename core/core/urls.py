"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
from accounts.views import CommonroomLoginView, logout_view, register
from home.views import (
    about,
    add_car,
    contact,
    delete_invite,
    home,
    invite_person,
    overview,
    success_page,
    toggle_car,
    toggle_member_status,
)

urlpatterns = [
    path('accounts/register/', register, name='register'),
    path('accounts/login/', CommonroomLoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('overview/', overview, name='overview'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('invite/', invite_person, name='invite'),
    path('invite/<int:invite_id>/delete/', delete_invite, name='delete_invite'),
    path('cars/add/', add_car, name='add_car'),
    path('cars/<int:car_id>/toggle/', toggle_car, name='toggle_car'),
    path('members/status/toggle/', toggle_member_status, name='toggle_member_status'),
    path('admin/', admin.site.urls),
    path('success/', success_page, name='success_page')
   
]
