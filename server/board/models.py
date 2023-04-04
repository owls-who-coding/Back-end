from django.db import models

#담당자가 작성한 db의 테이블이 아닌 모델들은. 이전 코드 작성중 db와 파이썬의 연결 과정에서
#자동으로 생성된 테이블임. db에만 생기고 모델은 따로 생기지 않았었는데,
#python manage.py inspectdb 명령어로 db를 감지하여 모델을 불러와서 생김.
#db모델을 전달할 때는 해당 테이블이 없는 상태라 만약 해당 모델에서 오류가 생기면 주석처리 해도 문제없음.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'
        app_label = 'board'

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
        app_label = 'board'

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)
        app_label = 'board'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        app_label = 'board'

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)
        app_label = 'board'

class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
        app_label = 'board'

class Comment(models.Model):
    comment_number = models.AutoField(primary_key=True)
    post_number = models.ForeignKey('Post', models.DO_NOTHING, db_column='post_number')
    before_comment = models.IntegerField(blank=True, null=True)
    user_number = models.ForeignKey('User', models.DO_NOTHING, db_column='user_number')
    comment_body_path = models.TextField()

    class Meta:
        managed = False
        db_table = 'comment'
        app_label = 'board'
        app_label = 'board'

class Disease(models.Model):
    disease_number = models.AutoField(primary_key=True)
    disease_name = models.CharField(unique=True, max_length=45)
    disease_imfomation_path = models.TextField()

    class Meta:
        managed = False
        db_table = 'disease'
        app_label = 'board'
        app_label = 'board'

    def __str__(self):
        return str(self.disease_number)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'
        app_label = 'board'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
        app_label = 'board'

class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
        app_label = 'board'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
        app_label = 'board'

class Post(models.Model):
    post_number = models.AutoField(primary_key=True)
    user_number = models.ForeignKey('User', models.DO_NOTHING, db_column='user_number')
    post_body_path = models.TextField()
    image_path = models.TextField()
    disease_number = models.ForeignKey('Disease', models.DO_NOTHING, db_column='disease_number')
    comment_count = models.IntegerField()
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'post'
        app_label = 'board'


class TestTable(models.Model):
    test_pk = models.IntegerField(primary_key=True)
    test_int = models.IntegerField(blank=True, null=True)
    test_var = models.CharField(max_length=45, blank=True, null=True)
    test_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_table'
        app_label = 'board'


class User(models.Model):
    user_number = models.AutoField(primary_key=True)
    id = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    age = models.IntegerField()
    dog_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user'
        app_label = 'board'

    def __str__(self):
        return str(self.user_number)


#Django REST Framework ( DRF ) 와 안드로이드 연동하기
class Version(models.Model):
    version = models.CharField(max_length=10)

    def __str__(self):
        return self.version
#serializers.py 부분까지