from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from users.models import Card


class IsKagisysHousing(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='kagisys').exists()


@login_required
@permission_classes(IsKagisysHousing)
@api_view(['GET'])
def get_all_idm(request):
    return Response(','.join(Card.objects.values_list('idm', flat=True)))
