"""
URL configuration for fundflowapplication project.

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
from django.urls import path
from fundflowbudget import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/all/', views.TransactionListView.as_view(), name='transactions-list'),
    path('transactions/add/', views.TransactionCreatedView.as_view(), name='transactions-add'),
    path('transactions/<int:pk>',views.TransactionDetailView.as_view(), name='transactions-detail'),
    path('transactions/<int:pk>/remove',views.TransactionDeleteView.as_view(), name='transactions-delete'),
    path('transactions/<int:pk>/change',views.TransactionUpdateView.as_view(),name='transactions-update'),
    path('signup/',views.SignUpView.as_view(), name='signup-view'),
    path('signin/',views.SignInView.as_view(), name='signin-view')
]
