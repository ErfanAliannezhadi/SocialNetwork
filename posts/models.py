from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    @property
    def slug(self):
        return slugify(self.title)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('posts:post',args=[self.id,self.slug])
    def is_liked(self,user):
        like = PostLike.objects.filter(user=user,post=self)
        if like.exists():
            return True
        return False
    def likescount(self):
        return self.pvotes.count()

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomments')
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment',on_delete=models.CASCADE,related_name='rcomments',blank=True,null=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} : {self.body[:10]}'

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.user} likes {self.post}'







