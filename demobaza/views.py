from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

from .models import Project, Track


def home(request):
    return render(request, 'home.html', {
        'projects': Project.objects.filter(is_active=True),
    })


def musician(request, slug):
    project = get_object_or_404(Project, slug__iexact=slug)
    music = Track.objects.filter(project=project.pk)
    return render(request, 'musician.html', {'musician': project, 'musics': music})


def login(request):
    context = RequestContext(request, {
        'request': request, 'user': request.user})
    return render_to_response('login.html', context_instance=context)


# @login_required(login_url='/')
def home(request):
    return render_to_response('home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
