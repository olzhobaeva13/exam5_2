
from django.contrib.auth import get_user_model
from posts.forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post
from django.views import View
User = get_user_model()


def posts_list_view(request):
    if request.user.is_authenticated:
        posts = request.user.posts.all()
    else:
        posts = Post.objects.all()

    return render(request, 'posts/index.html', context={'posts': posts})


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_detail.html', context={'post': post, })


class PostCreateView(View):
    form = PostForm
    template = 'posts/post_create.html'
    has_author = True

    def get(self, request):
        form = self.form()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect(obj)
        return render(request, self.template, context={'form': form})


class PostUpdateView(View):
    obj_class = Post
    template = 'posts/post_update.html'
    bound_form = PostForm

    def get(self, request, id):
        obj = get_object_or_404(self.obj_class, id=id)
        bound_form = self.bound_form(instance=obj)
        return render(request, self.template, context={'form': bound_form,
                                                       self.obj_class.__name__.lower(): obj})

    def post(self, request, id):
        obj = get_object_or_404(self.obj_class, id=id)
        bound_form = self.bound_form(request.POST, instance=obj)
        if bound_form.is_valid():
            post = bound_form.save()
            return redirect(post)
        return render(request, self.template, context={'form': bound_form,
                                                       self.obj_class.__name__.lower(): obj})


class PostDeleteView(View):
    obj_class = Post
    template = 'posts/post_delete.html'
    list_url = 'posts_list_url'

    def get(self, request, id):
        obj = get_object_or_404(self.obj_class, id=id)
        return render(request, self.template, context={self.obj_class.__name__.lower(): obj})

    def post(self, request, id):
        obj = get_object_or_404(self.obj_class, id=id)
        obj.delete()
        return redirect(reverse(self.list_url))

