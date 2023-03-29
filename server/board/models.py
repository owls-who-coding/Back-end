from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


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


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Post(models.Model):
    post_number = models.AutoField(primary_key=True)
    user_number = models.ForeignKey('User', models.DO_NOTHING, db_column='user_number')
    post_body_path = models.TextField()
    image_path = models.TextField()
    disease_number = models.ForeignKey(Disease, models.DO_NOTHING, db_column='disease_number')
    comment_count = models.IntegerField()
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

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

