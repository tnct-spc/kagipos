"""possys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from . import views as possys_views

urlpatterns = [
    path('', possys_views.products_list, name="products_list"),
    path('history/', possys_views.history, name="history"),
    path('add_transaction/<int:price>/<idm>/<int:product_id>/', possys_views.add_transaction_with_product),
    path('add_transaction/<int:price>/<idm>/', possys_views.add_transaction_without_product),
]
