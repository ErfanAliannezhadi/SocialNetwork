from django.shortcuts import render,redirect
from django.views import View
from .models import Post, Comment, PostLike
from django.contrib import messages
from .forms import PostupdateForm, CommentcreateForm, ReplycreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Postview(View):
    def setup(self, request, *args, **kwargs):
        return super().setup(request,*args, kwargs)
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(id=post_id)
        is_liked = post.is_liked(request.user)
        commentform = CommentcreateForm()
        replyform = ReplycreateForm()
        comments = post.pcomments.filter(is_reply=False)
        allcomments = post.pcomments.all()
        if post.slug == post_slug:
            return render(request,'posts/post.html',{'post':post,'comments':comments, 'commentform':commentform,
                                                     'replyform':replyform,'allcomments':allcomments,'is_liked':is_liked})
        return redirect('home:home')
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        form = CommentcreateForm(request.POST)
        post = Post.objects.get(id=kwargs['post_id'])
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request,'your comment submitted successfully','success')
            return redirect('posts:post', post.id, post.slug )
class Postdelete(LoginRequiredMixin,View):
    def get(self,request, post_id, post_slug):
        post = Post.objects.get(id=post_id)
        if post.slug == post_slug and post.user == request.user:
            post.delete()
            messages.success(request,'The post deleted successfully')
            return redirect('home:home')
        messages.error(request,'you can\'t delete this post','danger')
        return redirect('home:home')
class Postupdate(LoginRequiredMixin,View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.slug != kwargs['post_slug']:
            return redirect('home:home')
        if post.user != request.user:
            messages.error(request, 'you can\'t update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,post_id,post_slug):
        post = self.post_instance
        form = PostupdateForm(instance=post)
        return render(request,'posts/postupdate.html',{'form':form})
    def post(self,request,post_id,post_slug):
        post = self.post_instance
        form = PostupdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'you updated this post successfully','success')
        return redirect('posts:post', post.id,post.slug)
class Postcreate(LoginRequiredMixin,View):
    def get(self,request):
        form = PostupdateForm()
        return render(request,'posts/postcreate.html',{'form':form})
    def post(self,request):
        form = PostupdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Post.objects.create(title=data['title'],body=data['body'],user=request.user)
            messages.success(request,'you created a new post successfully','success')
            return redirect('posts:post', post.id , post.slug)
        return redirect('posts:post_create')

class AddReplyview(LoginRequiredMixin,View):
    def post(self,request,post_id,comment_id):
        form = ReplycreateForm(request.POST)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request,'your reply submitted successfully','success')
        return redirect('posts:post',post.id,post.slug)

class PostLikeView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(id=post_id)
        like = PostLike.objects.filter(user=request.user, post=post)
        if not like.exists():
            PostLike.objects.create(user=request.user, post=post)
        else:
            messages.warning(request,'you had liked this post','danger')
        return redirect('posts:post', post.id, post.slug)

class PostUnlikeView(View):
    def get(self,request,post_id):
        post = Post.objects.get(id=post_id)
        like = PostLike.objects.filter(post=post,user=request.user)
        if like.exists():
            like.delete()
        else:
            messages.warning(request,'you hadn\'t likes this post','danger')
        return redirect('posts:post', post.id, post.slug)