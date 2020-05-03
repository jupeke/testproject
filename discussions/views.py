from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Discussion, User, Topic, Post
from django.utils import timezone

# Create your views here.
from .forms import NewTopicForm, EditTopicForm, EditPostForm, PostForm
def home(request):
    discussions = Discussion.objects.all()
    return render(request, 'home.html', {'discussions': discussions})

# Param discussion_id is defined in the urls.py
def discussion_topics(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    return render(request, 'topics.html', {'discussion': disc})

# Param discussion_id and topic_id is defined in the urls.py
# Note discussion__pk with 2x "_" to get the current discussion primary key.
def topic_posts(request, discussion_id, topic_id):
    curr_topic = get_object_or_404 (Topic, discussion__pk=discussion_id, pk=topic_id)
    return render(request, 'topic_posts.html', {'topic': curr_topic})

# Note: this both shows a new topic form and saves a new topic. Seems to be
# the normal way with django.
@login_required
def new_topic(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)

    # POST -> user is submitting date to the server.
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.discussion = disc
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect(
                'url_topic_posts', discussion_id=disc.pk, topic_id=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'discussion': disc, 'form':form})

@login_required
def reply_topic(request, discussion_id, topic_id):
    topic = get_object_or_404(Topic, discussion__pk=discussion_id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Does not save into db
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect(
                'url_topic_posts',
                discussion_id=topic.discussion.pk,
                topic_id=topic.pk
            )
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# Note: this both shows a new topic form and saves a new topic. Seems to be
# the normal way with django.
@login_required
def edit_topic(request, discussion_id, topic_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    topic = get_object_or_404 (Topic, pk=topic_id)

    # POST -> user is submitting date to the server.
    if request.method == 'POST':
        form = EditTopicForm(request.POST, instance = topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.last_updated = timezone.now() # save did not do it automatically..
            topic.save()
            return redirect('url_discussion_topics', discussion_id=disc.pk)
    else:
        form = EditTopicForm(instance = topic)
    return render(request, 'edit_topic.html',
        {'discussion': disc, 'topic': topic, 'form':form})

@login_required
def edit_post(request, discussion_id, topic_id, post_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    topic = get_object_or_404 (Topic, pk=topic_id)
    post = get_object_or_404 (Post, pk=post_id)

    # POST -> user is submitting date to the server.
    if request.method == 'POST':
        form = EditPostForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect(
                'url_topic_posts',
                discussion_id=disc.pk,
                topic_id = topic.pk)
    else:
        form = EditPostForm(instance = post)
    return render(request, 'edit_post.html',
        {'discussion': disc, 'topic': topic, 'post': post, 'form':form})
