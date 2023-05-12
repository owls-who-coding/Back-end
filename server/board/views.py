import base64
import os

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework.response import Response

from .forms import PostForm #forms.py는 작성한 부분.
from datetime import datetime
from rest_framework import generics, viewsets
from rest_framework import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post, User, Disease, Comment
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
COMMENT_PATH='CommentData'

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}')

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}/dieasefile'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}/dieasefile')

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}/imagefile'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}/imagefile')

if not os.path.exists(f'{ROOT_PATH}/{DATA_PATH}/txtfile'):
    os.makedirs(f'{ROOT_PATH}/{DATA_PATH}/txtfile')



@api_view(['GET'])
def post_list(request):
    #posts = Post.objects.all()
    posts=Post.objects.all().order_by('-post_number')
    serializer = PostSerializer(posts, many=True)
   # print(serializer.data)
    return Response(serializer.data)


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

        # # 로그를 출력합니다.
        user = User.objects.get(pk=user_number)
        disease = Disease.objects.get(pk=disease_number)



        created_at = timezone.now()

        formatted_time = created_at.strftime('%y%m%d%H%M%S')

        file_name = f"{user_number} {formatted_time}"


        #jpg 파일로 저장.
        image = request.FILES.get('image', None)
        #logger.info("위치확인5")#여기까지 진행


        # txt 파일로 변환하여 저장
        #save_path = './testfile/txtfile'

        #file_name = 'testing888888' #수정 필요   부터 3줄의 원래 위치.

        #file_path = os.path.join(save_path, file_name)
        file_path = f'{ROOT_PATH}/{DATA_PATH}/txtfile/{file_name}.txt'
        #logger.info("위치확인 fiel_path")
        if image:
            #logger.info("위치확인6")
            fs = FileSystemStorage(location=f'{ROOT_PATH}/{DATA_PATH}/imagefile/')
            image_file_name = f'{file_name}.jpg'  # 이미지 확장자에 따라 변경해야 할 수 있습니다.
            filename = fs.save(image_file_name, image)
            image_path = f'{ROOT_PATH}/{DATA_PATH}/imagefile/{filename}'
            #logger.info("위치확인7")

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
                    updated_at=timezone.now())
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




#이미지와 텍스트 파일을 동시에 불러오는 view인데 이미지 파일이 없어도 되는 view. 이 코드가 게시글 불러오기에 성공한 가장 최신 버전
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
#위에 까지가 잘 작동하던 게시글 불러오기 view. 이하  view는 댓글도 같이 불러오는 기능을 추가하고 있음

# 최종 적으로 게시글과 댓글을 분리. 이하가 댓글을 불러오는 코드

class GetCommentsView(View):
    def get(self, request, post_number):

        all_comments = Comment.objects.filter(post_number=post_number).order_by('comment_number')

        logger.info("위치 확인: 쿼리셋 로그 시작")
        # all_comments 쿼리셋이 비어 있는지 확인하는 로그 추가
        if not all_comments.exists():
            logger.info("all_comments 쿼리셋이 비어 있습니다.")
        else:
            logger.info(f"all_comments 쿼리셋에 {all_comments.count()}개의 댓글이 있습니다.")
        logger.info("위치 확인: 쿼리셋 로그 완료")

        comments_data = self.build_comment_tree(all_comments)

        # 정렬: 먼저 before_comment 값으로 정렬하고, 그 다음 comment_id 값으로 정렬
        comments_data = sorted(comments_data, key=lambda x: (x['before_comment'], x['comment_id']))


        logger.info("위치 확인: 댓글 트리 생성 완료")
        response_data = {
            'comments': comments_data
        }
        return JsonResponse(response_data)

    def build_comment_tree(self, all_comments):
        comments_data = []

        for comment in all_comments:
            comment_author = comment.user
            comment_data = {
                'comment_id': comment.comment_number,
                'content': self.get_comment_content(comment),
                'author_name': comment_author.name,
                'before_comment': comment.before_comment,
            }
            comments_data.append(comment_data)

        return comments_data

    def get_comment_content(self, comment):
        text_file_path = f'{ROOT_PATH}/{COMMENT_PATH}/{comment.comment_body_path}.txt'
        logger.info(f"댓글 경로 확인: {text_file_path}")
        with open(text_file_path, 'r', encoding='utf-8') as f:
            comment_content = f.read()
        return comment_content


#로그인 기능을 담당하는 view 입니다.
@api_view(['POST'])
def login(request):
    if request.method == 'POST':

        id = request.data.get('id')
        password = request.data.get('password')

        # 로그 메시지 출력
        logger.info(f"Received login request with id: {id}, password: {password}")

        try:
            user = User.objects.get(id=id)  # 사용자 정의 User 모델에서 아이디를 검색
            logger.info(f"User found: {user}")
            logger.info(f"Entered password: {password}")
            logger.info(f"Stored password: {user.password}")
            logger.info(f"Stored user_number: {user.user_number}")
            logger.info(f"Stored user.name: {user.name}")
        except ObjectDoesNotExist:
            user = None
            logger.info(f"User not found for id: {id}")

        # 사용자가 존재하고 비밀번호가 일치하는 경우
        #if user is not None and user.password == password: #암호화 미사용.
        if user is not None and check_password(password, user.password):#암호화 사용

            response = {
                'success': True,
                'message': '로그인 성공',
                'user_number': user.user_number,
                'user_name': user.name,

            }
        else:
            response = {
                'success': False,
                'message': '로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.'
            }
            logger.info(f"Login failure for id: {id}")
        return JsonResponse(response)

#회원 가입을 위한 view입니다.
@api_view(['POST'])
@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        id = request.data.get('id')
        password = request.data.get('password')
        name = request.data.get('name')
        age = request.data.get('age')
        dog_name = request.data.get('dog_name')

        # 비밀번호 해싱
        hashed_password = make_password(password)

        # 사용자 생성
        user = User(id=id, password=hashed_password, name=name, age=age, dog_name=dog_name)
        user.save()

        response = {
            'success': True,
            'message': '회원가입 성공'
        }

        return JsonResponse(response)

#통신기능 시험을 위한 view 입니다. 개발 완료시 삭제예정 입니다.
def test(request):
    response_data = {"id":1,"title":"테스트 데이터."}
    print(JsonResponse(response_data))
    print(response_data)
    return JsonResponse(response_data)


