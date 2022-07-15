from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField(max_length=450)
    likes = models.ManyToManyField(User, related_name='blog_post')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def total_likes(self):
        return self.likes.count()

    def get_days(self):
        current = timezone.now()
        delta = current - self.created
        if delta.days <= 1:
            return f'{delta.days} day ago'
        else:
            return f'{delta.days} days ago'

    def __str__(self):
        return f'Post by {self.author.username}'

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=450)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='follower')    # me, person following
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='following')  # person being followed

    def __str__(self):
        return self.user.username


# create posts and followers will see
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.author
        followers = Follow.objects.all().filter(following=user) # all users following the current user
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


class FollowersCount(models.Model):
    follower = models.CharField(max_length=1000)    # me, person following
    user = models.CharField(max_length=1000)    # person being followed

    def __str__(self):
        return self.user


post_save.connect(Stream.add_post, sender=Post)
