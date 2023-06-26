from django.shortcuts import redirect
from .models import Post

def check_user(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                post = Post.objects.get(pk=kwargs['pk'])
                if not (post.author == request.user or request.user.is_moderator()):
                    return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)
    
        return _wrapped_view

    if function:
        return decorator(function)
    
    return decorator