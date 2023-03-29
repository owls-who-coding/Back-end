from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm #forms.py는 작성한 부분.
from datetime import datetime

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

@login_required
# views.py
def post_create(request):
    print("Post_create")
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # 파일 저장
            post_body_path = f'media/{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(post_body_path, 'w') as f:
                f.write(form.cleaned_data['body_text'])
            # 게시글 생성
            post = form.save(commit=False)
            post.author = request.user
            post.post_body_path = post_body_path
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})
