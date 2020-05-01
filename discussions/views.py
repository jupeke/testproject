from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Discussion, User, Topic, Post
from .forms import NewTopicForm
# Create your views here.
def home(request):
    discussions = Discussion.objects.all()
    return render(request, 'home.html', {'discussions': discussions})

# Param discussion_id is defined in the urls.py
def discussion_topics(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    return render(request, 'topics.html', {'discussion': disc})

# Note: this both shows a new topic form and saves a new topic. Seems to be
# the normal way with django.
@login_required
def new_topic(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    user = User.objects.first()

    # POST -> user is submitting date to the server.
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.discussion = disc
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('url_discussion_topics', discussion_id=disc.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'discussion': disc, 'form':form})
