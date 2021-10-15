from django.contrib import admin

from network.models import Comment, Follow, Followed, Follower, Like, Post, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_post', 'text_content', 'like_number','comment_number')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'follower_num')

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Followed)
admin.site.register(Follower)
admin.site.register(Follow, FollowAdmin)

