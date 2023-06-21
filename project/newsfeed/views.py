from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Post, Comments
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

# Create your views here.
@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    http_method_names = ['post']
    form_class = PostCreateForm
    template_name = 'home.html'
    success_url = reverse_lazy('feed:home')



@require_http_methods(['POST'])
def create_comment(request, post_id=None):
    post = Post.objects.get(id=post_id)
    comment = Comments(user=request.user, post=post, content=request.POST['content'])
    comment.save()
    return redirect('feed:home')