# from typing import Any, Dict
# from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.urls import reverse

from .models import Post, PostImage
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm

from django.contrib.auth.decorators import login_required
from .decorators import check_user

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
            
    
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        length = request.POST.get('length')
        title = request.POST.get('title')
        text = request.POST.get('text')

        post = Post.objects.create(
            title=title,
            text=text,  
            published_date = timezone.now(),
            author = request.user
        )

        for file_num in range(0, int(length)):
            PostImage.objects.create(
                post = post,
                image = request.FILES.get(f'images{file_num}')
            )

        response_data = {
            'redirect_url': reverse('post_detail', kwargs={'pk': post.pk})
        }
        return JsonResponse(response_data)
    
    else:
        return render(request, 'blog/post_edit.html')

@check_user
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        length = request.POST.get('length')
        title = request.POST.get('title')
        text = request.POST.get('text')

        post.title = title
        post.text = text
        post.published_date = timezone.now()
        post.save()
        post.delete_related_images()
        
        for file_num in range(0, int(length)):
            PostImage.objects.create(
                post = post,
                image = request.FILES.get(f'images{file_num}')
            )

        response_data = {
            'redirect_url': reverse('post_detail', kwargs={'pk': post.pk})
        }
        return JsonResponse(response_data)
    else:
        return render(request, 'blog/post_edit.html', {'post': post})

@check_user
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    return render(request, 'blog/post_delete.html')

class Search(ListView):

    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(title__iregex=self.request.GET.get( 'search' ))
    
    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        content['search'] = self.request.GET.get( 'search' )
        return content