"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import router#router.urls 사용하기 위해 import
from django.http import HttpResponse
from django.template.defaulttags import url# url() 추가한거 사용하기 위해 import
from django.urls import path, include, re_path
from rest_framework import routers

from board import views
from board.views import post_list


router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
#오류 탐색을 위한 함수
def log_request(request, *args, **kwargs):
    print(request.get_full_path())
    return HttpResponse("Logged.")
#오류 없으면 지워도 됨.


urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-post/', views.create_post, name='create_post'),  # 실제 엔드포인트를 입력하세요.
    path('', include(router.urls)),
    path('posts/test', views.test, name='test'),
    path('post/', post_list, name='post-list'),
    path('login/', views.login, name='login'),#로그인 view로 이어지는 url입니다.
    path('sign_up/', views.sign_up, name='sign_up'),
    path('update-post/', views.update_post, name='update_post'),#게시글 수정 url
    # path('api/posts/<str:post_body_path>/content', views.get_post_content, name='get_post_content'),
    #위는 기존의 텍스트만 불러오는 url, 아래쪽은 이미지와 같이 불러오는 url
    path('api/posts/<str:post_body_path>/content_and_image', views.get_post_and_image_content, name='get_post_and_image_content'),
    path('api/posts/<int:post_number>/comments', views.GetCommentsView.as_view(), name='GetCommentsView'),
    #이하 코드는 게시글 삭제 url
    path('delete-post/', views.delete_post, name='delete_post'),  # 게시글 삭제 url
    #이하의 url은 댓글도 불러오는 view를 연결한 url. 실패하여 view 삭제 시 위의 url을 유지
    # path('api/posts/<str:post_body_path>/<int:post_number>/content_and_image',
    #      views.GetPostDataWithCommentsView.as_view(),
    #      name='get_post_and_image_content_with_comments'),

    path('ai_api/', include('ai_api.urls'))
    #re_path(r'^.*$', log_request, name='log_request'),  # 이 줄을 urlpatterns 리스트의 마지막에 추가하세요.


    #Django REST Framework ( DRF ) 와 안드로이드 연동하기
    # url(r'^', include(router.urls)),
    # url(r'^api-v1/', include('rest_framework.urls', namespace='rest_framework_category')),
    #Django REST Framework ( DRF ) 와 안드로이드 연동하기
]

# restApi 용도
# urlpatterns = [
#     path('api/posts/', views.PostList.as_view()),
#     path('api/posts/new/', views.PostCreate.as_view()),
#     path('api/posts/<int:pk>/', views.PostDetail.as_view()),
# ]