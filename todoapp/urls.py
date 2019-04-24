"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from app.views import loginUser,register,dashboard,logoutUser,newtask,details,update,delete,share,comments,deletecoment,updatecoment


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register , name="register"),
    path('login/',loginUser,name="login"),
    path('dashboard/',dashboard, name="dashboard"),
    path('logout/',logoutUser,name="logout"),
    path('newtask/',newtask,name="newtask"),
    path('',register),
    path('details/<int:pk>',details,name="details"),
    path('update/<int:pk>',update,name="update"),
    path('delete/<int:pk>',delete,name="delete"),
    path('share/<int:pk>',share,name="share"),
    path('comments/<int:pk>',comments,name="comments"),
    path('deletecoment/<int:pk>',deletecoment,name="deletecoment"),
    path('updatecoment/<int:pk>',updatecoment,name="updatecoment"),

    
]
