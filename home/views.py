from django.shortcuts import render
from django.views import View
from posts.models import Post
from .forms import PostSearchForm


class HomePage(View):
    def get(self, request):
        posts = Post.objects.all()
        form = PostSearchForm()
        if request.GET.get('search'):
            posts = posts.filter(title__contains=request.GET['search'])
        return render(request, 'home/home.html', {'posts': posts, 'form': form})
