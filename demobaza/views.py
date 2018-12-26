from django.shortcuts import render
from demobaza.models import Project


def home(request):
    project_data = Project.objects.filter(is_active=True)
    return render(request, 'demobaza/home.html', context={'projects': project_data})
