from io import DEFAULT_BUFFER_SIZE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Value
from django.db.models.fields import IntegerField
from django.db.models.fields.files import ImageField


class User(AbstractUser):
    def __str__(self):
        return self.username
    def serialize(self):
        return{
            "id": self.id,
            "user": self.username,
            "email": self.email}

class Post(models.Model):
    user_post = models.ForeignKey(User, default=None, on_delete=CASCADE, related_name="post") #related_name eg: harry.post.all() <= show all of harry's post
    text_content = models.CharField(max_length=500)
    like_number = models.IntegerField(default=0)
    comment_number = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)

    def serialize_json(self):
        return{
            "id": self.id,
            "user": self.user_post.username,
            "user_id": self.user_post.id,
            "email": self.user_post.email,
            "content": self.text_content,
            "like": self.like_number,
            "comment": self.comment_number,
            "time": self.post_time.strftime('%B %d/ %H:%M')
        }

    def __str__(self):
        return self.text_content

class Comment(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=CASCADE)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, default=None, on_delete=CASCADE)

    def __str__(self):
        return f'{self.post} commented by {self.user}: {self.content}'

class Like(models.Model):
    post = models.OneToOneField(Post, default=None, on_delete=CASCADE)
    user = models.ManyToManyField(User, default=None, blank=True)

    def __str__(self):
        return f'{self.id}| {self.user.all().count()} | {self.post}'
    def serialize_json(self):
        users = self.user.all()
        data = [user.serialize() for user in users]
        return{
            "id": self.id,
            "post_id": self.post.id,
            "post": self.post.text_content,
            "every_likes": data,
            "likes_number": self.user.all().count(),
            
        }

class Follower(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=CASCADE)

    def __str__(self):
        return self.user.username

class Followed(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=CASCADE)
    follower = models.ForeignKey(Follower, default=None, related_name="follow", on_delete=CASCADE)
    button_value = models.CharField(default='Unfollow', max_length=8)
    def serialize_json(self):
        return{
            'id': self.id,
            'user': self.user.username,
            'follower': self.follower.user.username,
            'follower_id': self.follower.user.id,
            'followed_id': self.user.id,
            'button_value': self.button_value

        }

    def __str__(self):
        return f'{self.user.username}: is followed by {self.follower.user}'

class Follow(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=CASCADE)
    follower_num = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.user.id,
            "user": self.user.username,
            "follower": self.follower_num
        }
    
    