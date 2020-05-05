from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Discussion, User, Topic, Post
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.views.generic import UpdateView, ListView

from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

# Create your views here.
from .forms import NewTopicForm, EditTopicForm, EditPostForm, PostForm

def home(request):
    discussions = Discussion.objects.all()
    return render(request, 'home.html', {'discussions': discussions})

# Param discussion_id is defined in the urls.py
# This works but the class approach is now used instead.
def discussion_topics(request, discussion_id):
    disc = get_object_or_404 (Discussion, pk=discussion_id)
    '''
    This is a very interestin way of ordering the topics. At the same time
    a new column 'numbOfReplies' is created on the go. See topics.html.
    '''
    topics_of_discussion = \
        disc.topics.order_by('-last_updated'). \
            annotate(numbOfReplies=Count('posts')-1)

    # Setting up pagination. First gets the page number:
    page_numb = request.GET.get('page',1)
    paginator = Paginator(topics_of_discussion, 5)
    try:
        topics_paginated = paginator.page(page_numb)
    except PageNotAnInteger:
        #Fallback to the first page:
        topics_paginated = paginator.page(1)
    except EmptyPage:
        #Fallback to the last page:
        topics_paginated = paginator.page(paginator.num_pages)

    # Note that the names 'in quotes' are available in the topics.html:
    return render(request, 'topics.html',
        {'discussion': disc, 'topics': topics_paginated})

# This does the same as function above:
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        kwargs['discussion'] = self.discussion
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.discussion = get_object_or_404(
            Discussion, pk=self.kwargs.get('discussion_id'))
        topics_of_discussion = \
            self.discussion.topics.order_by('-last_updated'). \
                annotate(numbOfReplies=Count('posts')-1)
        return topics_of_discussion

# Param discussion_id and topic_id is defined in the urls.py
# Note discussion__pk with 2x "_" to get the current discussion primary key.
def topic_posts(request, discussion_id, topic_id):
    curr_topic = get_object_or_404 (Topic, discussion__pk=discussion_id, pk=topic_id)

    # One added always someone loads the page showing the post:
    curr_topic.views += 1
    return render(request, 'topic_posts.html', {'topic': curr_topic})
    curr_topic.save()


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

'''
Below works but the class approach has its advantages.
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
'''
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'    # used in url
    context_object_name = 'post' # Default name 'object'

    # Overrides the method of parent class to add filter for
    # logged in user:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    # Overriding method to set extra fields
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        topic = post.topic
        topic.last_updated = timezone.now()
        topic.save()
        return redirect(
            'url_topic_posts',
            discussion_id=topic.discussion.pk,
            topic_id=topic.pk)
