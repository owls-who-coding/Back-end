import base64
import os

from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
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
from django.utils import timezone
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

#html 사용할 때 사용하던 코드로 추정. 기능 개발 하다가 문제 없으면 그대로 삭제.
# @login_required
# # views.py
# def post_create(request):
#     print("Post_create")
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             # 파일 저장
#             post_body_path = f'media/{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
#             with open(post_body_path, 'w') as f:
#                 f.write(form.cleaned_data['body_text'])
#             # 게시글 생성
#             post = form.save(commit=False)
#             post.author = request.user
#             post.post_body_path = post_body_path
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'post_form.html', {'form': form})
#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'post_detail.html', {'post': post})


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    print(serializer.data)
    return Response(serializer.data)

# #게시글을 파일로 변환하여 보관하는 view입니다.
# @csrf_exempt
# def create_post(request):
#     if request.method == 'POST':
#
#         logger.info("create_post 실행확인")
#         # 데이터를 받아옵니다.
#         text = request.POST.get('text', '')
#         title = request.POST.get('title', '')
#         user_number = int(request.POST.get('user_number', ''))
#         disease_number = int(request.POST.get('disease_number', ''))
#         # 로그를 출력합니다.
#         logger.info(f"text: {text}")
#         logger.info(f"user_number: {user_number}")
#         logger.info(f"disease_number: {disease_number}")
#         logger.info(f"title: {title}")
#         logger.info("실행확인")
#         user = User.objects.get(pk=user_number)
#         disease = Disease.objects.get(pk=disease_number)
#
#
#
#         # txt 파일로 변환하여 저장
#         #save_path = './testfile/txtfile'
#
#         # file_name = 'testing888888' #수정 필요
#         created_at = datetime.now()
#         formatted_time = created_at.strftime('%y%m%d%H%M%S')
#         file_name = f"{user_number} {formatted_time}"
#
#         #file_path = os.path.join(save_path, file_name)
#         file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{file_name}.txt'
#
#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(text)
#
#         # Post 객체를 생성하고 데이터베이스에 저장합니다.
#         post = Post(user_number=user,
#                     disease_number=disease,
#                     post_body_path=file_name,
#                     image_path='',
#                     comment_count=0,
#                     title=title,
#                     created_at=created_at,
#                     updated_at=datetime.now())
#         post.save()
#
#         return JsonResponse({'message': 'Post created successfully'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

# 이미지 파일 넣었던 코드
@csrf_exempt
def create_post(request):
    if request.method == 'POST':

        logger.info("create_post 실행확인")
        # 데이터를 받아옵니다.
        text = request.POST.get('text', '')
        title = request.POST.get('title', '')
        user_number = int(request.POST.get('user_number', ''))
        disease_number = int(request.POST.get('disease_number', ''))

        # 로그를 출력합니다.
        logger.info(f"text: {text}")
        logger.info(f"user_number: {user_number}")
        logger.info(f"disease_number: {disease_number}")
        logger.info(f"title: {title}")
        logger.info("실행확인")
        user = User.objects.get(pk=user_number)
        disease = Disease.objects.get(pk=disease_number)

        logger.info("위치확인1")
        # file_name = 'testing888888' #수정 필요
        created_at = timezone.now()
        logger.info(created_at)#여기까지 진행

        formatted_time = created_at.strftime('%y%m%d%H%M%S')

        file_name = f"{user_number} {formatted_time}"


        #jpg 파일로 저장.
        image = request.FILES.get('image', None)
        logger.info("위치확인5")#여기까지 진행


        # txt 파일로 변환하여 저장
        #save_path = './testfile/txtfile'

        #file_name = 'testing888888' #수정 필요   부터 3줄의 원래 위치.

        #file_path = os.path.join(save_path, file_name)
        file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{file_name}.txt'
        logger.info("위치확인 fiel_path")
        if image:
            logger.info("위치확인6")
            fs = FileSystemStorage(location=f'{ROOT_PATH}/{DATA_PATH}/imagefile/')
            image_file_name = f'{file_name}.jpg'  # 이미지 확장자에 따라 변경해야 할 수 있습니다.
            filename = fs.save(image_file_name, image)
            image_path = f'{ROOT_PATH}/{DATA_PATH}/imagefile/{filename}'
            logger.info("위치확인7")

            # 이미지 처리 상태 로그 추가
            logger.info(f"Image received: {image}")
            logger.info(f"Image saved as: {filename}")
            logger.info(f"Image path: {image_path}")
        else:
            image_path = ''
            logger.info("No image received")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        # Post 객체를 생성하고 데이터베이스에 저장합니다.
        post = Post(user_number=user,
                    disease_number=disease,
                    post_body_path=file_name,
                    image_path=file_name,
                    comment_count=0,
                    title=title,
                    created_at=created_at,
                    updated_at=timezone.now())#여기 문제가 아니라는건 알았음
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



#텍스트 파일의 내용을 읽는 view입니다.  프론트 다 개발 후 해당 기능 완전히 개발하면 삭제 예정.
# def get_post_content(request, post_body_path):
#     logger.info("get_post_content 실행 확인")
#     logger.info(f"post_body_path: {post_body_path}")
#     try:
#         # 파일의 이름만 받았다고 가정하고, 실제 파일이 있는 경로를 지정합니다.
#
#         #수정 필요
#         file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{post_body_path}.txt'
#         logger.info(file_path)
#         # 파일을 열고 내용을 읽습니다.
#         with open(file_path, 'r', encoding='utf-8') as f:
#             content = f.read()
#             logger.info(content)
#
#
#         # 파일의 내용을 JSON 형식으로 반환합니다.
#         return JsonResponse({'content': content})
#
#
#
#     except Exception as e:
#
#         logger.error(f"Error: {str(e)}")
#
#         return JsonResponse({'error': str(e)}, status=500)


#이미지와 텍스트 파일을 동시에 불러오는 view인데 이미지 파일이 없어도 되는 view
def get_post_and_image_content(request, post_body_path):
    try:
        # 텍스트 파일 내용을 불러옵니다.
        text_file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{post_body_path}.txt'
        with open(text_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 이미지 파일이 있는지 확인합니다.
        image_file_path = f'{ROOT_PATH}/{DATA_PATH}/imagefile/{post_body_path}.jpg'

        if os.path.exists(image_file_path):
            # 이미지 파일이 있는 경우 base64로 인코딩합니다.
            with open(image_file_path, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            # 이미지 파일이 없는 경우 빈 문자열 반환
            image_base64 = ""

        return JsonResponse({'content': content, 'image_base64': image_base64})

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

#로그인 기능을 담당하는 view 입니다.
@api_view(['POST'])
def login(request):
    if request.method == 'POST':

        id = request.data.get('id')
        password = request.data.get('password')

        user = authenticate(request, username=id, password=password)

        if user is not None:
            response = {
                'success': True,
                'message': '로그인 성공',
                'user_id': user.id,
                'user_name': user.name,
            }
        else:
            response = {
                'success': False,
                'message': '로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.'
            }
        return JsonResponse(response)

#통신기능 시험을 위한 view 입니다. 개발 완료시 삭제예정 입니다.
def test(request):
    response_data = {"id":1,"title":"테스트 데이터."}
    print(JsonResponse(response_data))
    print(response_data)
    return JsonResponse(response_data)


