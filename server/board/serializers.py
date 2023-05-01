from rest_framework import serializers

from board.models import Version, Post, Disease, Comment
# 여기부터 USER API제공을 위해 추가함
from board.models import Version
from django.contrib.auth.models import User


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_number', 'id', 'name', 'age', 'dog_name')


# class PostSerializer(serializers.ModelSerializer):
#     user_number = UserSerializer()
#     disease_number = DiseaseSerializer()
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#
# from rest_framework import serializers
# 위에가 기존
class PostSerializer(serializers.ModelSerializer):
    user_number = serializers.StringRelatedField()
    disease_number = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'

# CommentSerializer를 추가. 아직 시험중
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_number')  # user 필드에 user_number에 해당하는 User 정보를 저장합니다.

    class Meta:
        model = Comment
        fields = ('comment_number', 'post_number', 'before_comment', 'user', 'comment_body_path')
        # user 필드를 추가하여 Comment 정보와 연관된 User 정보도 함께 전송하게 됩니다.
# 여기까지

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('version',)
