from django.shortcuts import render

from .models import Project


def home(request):
    return render(request, 'home.html', {
        'projects': Project.objects.filter(is_active=True),
    })
