from django.shortcuts import render
from .models import Post
from .models import Comment
from django.utils import timezone
from .forms import PostForm
from .forms import CommentForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request,'blog/post_list.html',{'posts':posts})


def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    comments=Comment.objects.filter(post=pk).order_by('created_date')
    return render(request,'blog/post_detail.html',{'post':post,'comments':comments})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author =request.user 
           # post.published_date=timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form=PostForm()


    return render(request,'blog/add_post.html',{'form':form})

@login_required
def add_comment(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == "POST":
       form=CommentForm(request.POST)
       if form.is_valid():
          comment=form.save(commit=False)
          comment.author=request.user
          comment.post=post     
          #comment.approve() 
          comment.published_date=timezone.now()
          comment.save()
          return redirect('post_detail',pk=post.pk) 

    else:
        form=CommentForm() 

    return render(request,'blog/add_comment.html',{'form':form})  

@login_required
def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author =request.user 
           # post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm(instance=post)


    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    a=request.user 
    b=post.author 
    if a==b:
       post.publish()
       return redirect('post_list')
    else:
       return redirect('post_detail',pk=pk) 

@login_required
def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    a=request.user 
    b=post.author 
    if a==b:
       post.delete()
       return redirect('post_list')
    else:
       return redirect('post_detail',pk=pk) 
       
    
    

    

       



