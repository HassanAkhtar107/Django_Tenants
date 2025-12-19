# from django.shortcuts import render
# from .models import Campus
# import logging
# logger = logging.getLogger(__name__)
# def project_list(request):
#     projects=Campus.objects.prefetch_related('departments').all()
#     logger.info(f"Retrieved projects: {projects}")
#     return render(request, 'campus/campus-list.html', {'projects': projects})