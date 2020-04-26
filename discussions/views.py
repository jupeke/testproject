from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Discussion
# Create your views here.
def home(request):
    discussions = Discussion.objects.all()
    return render(request, 'home.html', {'discussions': discussions})

# Param discussion_id is defined in the urls.py
def discussion_topics(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    return render(request, 'topics.html', {'discussion': disc})
