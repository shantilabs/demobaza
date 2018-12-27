from django.shortcuts import render

from .models import Project, Track


def home(request):
    return render(request, 'home.html', {
        'projects': Project.objects.filter(is_active=True),
    })


def musician(request, slug):
    project = Project.objects.filter(slug=slug).first()
    music = Track.objects.filter(project=project.pk)
    return render(request, 'musician.html', {'musician': project, 'musics': music})

