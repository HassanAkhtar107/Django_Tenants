from rest_framework import generics
from django.shortcuts import render
from .models import Campus
from .serializers import CampusSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging
logger = logging.getLogger(__name__)
def project_list(request):
    projects=Campus.objects.prefetch_related('departments').all()
    logger.info(f"Retrieved projects: {projects}")
    return render(request, 'campus/campus-list.html', {'projects': projects})

class CampusTenantData(generics.ListAPIView):
    serializer_class=CampusSerializer
    permission_classes=(IsAuthenticated,)
    queryset=Campus.objects.prefetch_related('departments').all()