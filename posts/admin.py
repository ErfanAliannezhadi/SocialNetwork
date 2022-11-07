from django.contrib import admin
from posts.models import Post,Comment, PostLike

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','updated']
    search_fields = ['title','body']
    list_filter = ['user','updated']
    raw_id_fields = ['user']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','user','created']
    list_filter = ['user','post']
    raw_id_fields = ['user','post',]

admin.site.register(Post, PostAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(PostLike)