from django.urls import path, re_path, include
from . import views as kagisys_views

urlpatterns = [
    path('get_all_idm/', kagisys_views.get_all_idm),
]
