from rest_framework import serializers

from board.models import Version, Post, Disease
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



# 여기까지

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('version',)
