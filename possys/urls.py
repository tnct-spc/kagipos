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
from django.urls import path
from rest_framework import routers

from . import views as possys_views

urlpatterns = [
    path('', possys_views.StoreView.as_view(), name="store"),
    path('history/', possys_views.HistoryView.as_view(), name="history"),
    path('api/add_transaction/<idm>/<int:product_id>/', possys_views.add_transaction_with_product),
    path('api/add_transaction/<idm>/<int:price>/', possys_views.add_transaction_without_product),
]

router = routers.SimpleRouter()
router.register(r'possys/products', possys_views.ProductViewSet)
router.register(r'possys/categories', possys_views.CategoryViewSet)
