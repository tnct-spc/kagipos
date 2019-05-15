"""kagipos URL Configuration

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
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from possys.urls import router as possys_router


router = routers.DefaultRouter()
router.registry.extend(possys_router.registry)

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('store'))),
    path('admin/', admin.site.urls),
    path('kagisys/', include('kagisys.urls')),
    path('possys/', include('possys.urls')),
    path('accounts/', include('users.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', obtain_auth_token),
]
