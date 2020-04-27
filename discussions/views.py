from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from .models import Discussion, User, Topic, Post
# Create your views here.
def home(request):
    discussions = Discussion.objects.all()
    return render(request, 'home.html', {'discussions': discussions})

# Param discussion_id is defined in the urls.py
def discussion_topics(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    return render(request, 'topics.html', {'discussion': disc})

# Note: this both shows a new topic form and saves a new topic!
def new_topic(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: get the currently logged in user

        topic = Topic.objects.create(
            subject=subject,
            discussion=disc,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('url_discussion_topics', discussion_id=disc.pk)

    return render(request, 'new_topic.html', {'discussion': disc})
