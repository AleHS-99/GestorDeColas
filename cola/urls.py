"""cola URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from home.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomePage.as_view(),name="HomePage"),
    path('accounts/login/',LoginFormView.as_view(),name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('register',CreateUserForm.as_view(),name='register'),
    path('cola/add',AddCola.as_view(),name='AddCola'),
    path('cola/editar/<int:pk>/',EditCola.as_view(),name='EditCola'),
    path('cola/eliminar/<int:pk>/',DeleteCola.as_view(),name='DeleteCola'),
    path('listado/<int:pk>/',List_Control.as_view(),name="ListControl"),
    path('listado/add/<int:pk>/',AddColaItem.as_view(),name='ListAdd'),
    path('listado/edit/<int:pk>/', EditColaItem.as_view(), name='ListEdit'),
    path('listado/delete/<int:pk>/', DeleteColaItem.as_view(), name='ListDelete'),

]
