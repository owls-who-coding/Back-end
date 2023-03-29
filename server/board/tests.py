from django.test import TestCase

# Create your tests here.
from django.db import models

class Comment(models.Model):
    comment_number = models.AutoField(primary_key=True)
    post_number = models.ForeignKey('Post', models.DO_NOTHING, db_column='post_number')
    before_comment = models.IntegerField(blank=True, null=True)
    user_number = models.ForeignKey('User', models.DO_NOTHING, db_column='user_number')
    comment_body_path = models.TextField()

    class Meta:
        managed = False
        db_table = 'comment'


class Disease(models.Model):
    disease_number = models.AutoField(primary_key=True)
    disease_name = models.CharField(unique=True, max_length=45)
    disease_imfomation_path = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'disease'


class Post(models.Model):
    post_number = models.AutoField(primary_key=True)
    user_number = models.ForeignKey('User', models.DO_NOTHING, db_column='user_number')
    post_body_path = models.TextField()
    image_path = models.TextField()
    disease_number = models.ForeignKey(Disease, models.DO_NOTHING, db_column='disease_number')
    comment_count = models.IntegerField()
    title=models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'post'


class TestTable(models.Model):
    test_pk = models.IntegerField(primary_key=True)
    test_int = models.IntegerField(blank=True, null=True)
    test_var = models.CharField(max_length=45, blank=True, null=True)
    test_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_table'


class User(models.Model):
    user_number = models.AutoField(primary_key=True)
    id = models.CharField(max_length=45)
    passwerod = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    age = models.IntegerField()
    dog_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user'


# Create your models here.
