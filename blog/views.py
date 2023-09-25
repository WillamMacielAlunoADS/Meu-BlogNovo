from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from .models import Post, Categoria


def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    posts = reversed(posts)

    busca = request.GET.get('busca')
    if busca:
        posts = Post.objects.filter(categoria = busca)
        
    return render(request, 'blog/post_list.html', {'posts': posts, 'busca': busca})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.categoria = request.POST.get('categoria')
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    cats = Categoria.objects.filter(pub_date__lte=timezone.now())
    return render(request, 'blog/post_edit.html', {'form': form,'cats': cats})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":    
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
    
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
