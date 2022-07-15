from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Post, Comment, Stream, Follow, FollowersCount


class CreatePost(LoginRequiredMixin, View):
    def get(self, request):
        message = request.GET.get('message', None)
        liked = False
        post = Post.objects.create(author=request.user, body=message)
        if post.likes.filter(id=request.user.id).exists():
            liked = True

        streams = Stream.objects.filter(user=request.user)
        group_ids = []
        for stream in streams:
            group_ids.append(stream.id)
        post_item = Post.objects.filter(id__in=group_ids).all().order_by('-created')

        posts = []
        data = {}
        for i in range(len(post_item)):
            post_msg = {
                'id': post_item[i].id,
                'author': post_item[i].author.username,
                'body': post_item[i].body,
                'created': post_item[i].created,
                'likes': post_item[i].likes.all,
            }
            posts.append(post_msg)
        data['post_details'] = posts
        data['liked'] = liked
        print(data)
        return JsonResponse(data)


def followers_count(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'Follow':
            followers_cnt = FollowersCount.objects.create(follower=follower, user=user)
            followers_cnt.save()
        else:
            followers_cnt = FollowersCount.objects.get(follower=follower, user=user)
            followers_cnt.delete()
        return render(request, 'blog/index.html')


def index(request):
    current_user = request.GET.get('user')
    logged_in_user = request.user.username
    user_followers = len(FollowersCount.objects.filter(user=current_user))
    user_following = len(FollowersCount.objects.filter(follower=current_user))

    # get list of all followers of current user
    user_follow = FollowersCount.objects.filter(user=current_user)
    user_f = []
    for i in user_follow:
        user_follow = i.follower
        user_f.append(user_follow)
    if logged_in_user in user_f:
        follow_button = 'Unfollow'
    else:
        follow_button = 'Follow'
    context = {
        'current_user': current_user,
        'user_followers': user_followers,
        'user_following': user_following,
        'follow_button': follow_button
    }
    return render(request, 'blog/index.html', context)