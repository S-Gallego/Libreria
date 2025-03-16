"""
URL configuration for library_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoints para Bibliotecas
    path('libraries/', views.library_list, name='library_list'),
    path('libraries/<int:id>/', views.library_detail, name='library_detail'),

    # Endpoints para Libros
    path('books/', views.book_list, name='book_list'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
    path('libraries/<int:id>/books/', views.books_by_library, name='books_by_library'),

    # Endpoints para Usuarios
    path('users/', views.user_list, name='user_list'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),

    # Endpoints para Préstamos
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/<int:id>/', views.loan_detail, name='loan_detail'),
    path('users/<int:id>/loans/', views.user_loans, name='user_loans'),
]
