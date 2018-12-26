from django.shortcuts import render
from demobaza.models import Project


def home(request):
    project_data = list(Project.objects.all())
    return render(request, 'demobaza/home.html', context={'projects': project_data})
