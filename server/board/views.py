import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response

from .forms import PostForm #forms.py는 작성한 부분.
from datetime import datetime
from rest_framework import generics, viewsets
from rest_framework import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post, User, Disease
from .serializers import UserSerializer, PostSerializer
from django.core.serializers.json import DjangoJSONEncoder
import logging

logger = logging.getLogger(__name__)

#규철이형 노트북
#ROOT_PATH = 'C:/Users/98rbc/Desktop/owls_who_coding/Back-end/server/board'

#기본 베이스
ROOT_PATH = './board'
#데이터 저장할 폴더
DATA_PATH = 'PostData'

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}')

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}/dieasefile'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}/dieasefile')

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}/imagefile'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}/imagefile')

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}/txtfile'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}/txtfile')

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


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    print(serializer.data)
    return Response(serializer.data)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':

        logger.info("create_post 실행확인")
        # 데이터를 받아옵니다.
        text = request.POST.get('text', '')
        user_number = int(request.POST.get('user_number', ''))
        disease_number = int(request.POST.get('disease_number', ''))
        # 로그를 출력합니다.
        logger.info(f"text: {text}")
        logger.info(f"user_number: {user_number}")
        logger.info(f"disease_number: {disease_number}")
        logger.info("실행확인")
        user = User.objects.get(pk=user_number)
        disease = Disease.objects.get(pk=disease_number)


        # txt 파일로 변환하여 저장
        #save_path = './testfile/txtfile'

        file_name = 'testing888888.txt' #수정 필요

        #file_path = os.path.join(save_path, file_name)
        file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{file_name}.txt'

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        # Post 객체를 생성하고 데이터베이스에 저장합니다.
        post = Post(user_number=user,
                    disease_number=disease,
                    post_body_path=file_name,
                    image_path='',
                    comment_count=0,
                    title=text,
                    created_at=datetime.now(),
                    updated_at=datetime.now())
        post.save()

        return JsonResponse({'message': 'Post created successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('user_number', 'disease_number')
    serializer_class = PostSerializer


def get_post_content(request, post_body_path):
    logger.info("get_post_content 실행 확인")
    logger.info(f"post_body_path: {post_body_path}")
    try:
        # 파일의 이름만 받았다고 가정하고, 실제 파일이 있는 경로를 지정합니다.

        #수정 필요
        file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{post_body_path}.txt'
        logger.info(file_path)
        # 파일을 열고 내용을 읽습니다.
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(content)


        # 파일의 내용을 JSON 형식으로 반환합니다.
        return JsonResponse({'content': content})



    except Exception as e:

        logger.error(f"Error: {str(e)}")

        return JsonResponse({'error': str(e)}, status=500)


def test(request):
    response_data = {"id":1,"title":"테스트 데이터."}
    print(JsonResponse(response_data))
    print(response_data)
    return JsonResponse(response_data)



