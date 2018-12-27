from django.shortcuts import render

from .models import Project


def home(request):
    return render(request, 'home.html', {
        'projects': Project.objects.filter(is_active=True),
    })


def musician(request, slug):
    return render(request, 'musician.html', {'musician': Project.objects.filter(slug=slug).first()})

