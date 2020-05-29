from django.shortcuts import render
from .models import Post, Comment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Create your views here.


#comentar un post
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#registrar nuevo usuario
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

#metodos para aprobar o elimitar comentarios en espera de aprobación
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

#metodos para mostrar post
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    return render(request, "blog/post_list.html", {"posts":posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post":post})

#crear nuevo post
@login_required
def post_new(request):
    if request.method == "POST": 
        form = PostForm(request.POST) 
        if form.is_valid(): 
            post = form.save(commit=False) 
            post.author = request.user 
            post.save() 
            return redirect('post_detail', pk=post.pk) 
    else: 
        form = PostForm() 
    return render(request, 'blog/post_edit.html', {'form': form}) 

# metodo para editar un post o borrador
@login_required
def post_edit(request, pk): 
    post = get_object_or_404(Post, pk=pk) 
    if request.method == "POST": 
        form = PostForm(request.POST, instance=post) 
        if form.is_valid(): 
            post = form.save(commit=False) 
            post.author = request.user 
            post.save() 
            return redirect('post_detail', pk=post.pk)
    else: 
        form = PostForm(instance=post) 
    return render(request, 'blog/post_edit.html', {'form': form}) 


# metodos para mostrar, publicar o eliminar borradores de post
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
    return render(request, "blog/post_draft_list.html", {"posts": posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def inicio(request):
    return render(request, 'blog/inicio.html')