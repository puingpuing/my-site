from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notice(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User, on_delete=models.CASCADE,to_field='username', verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    view = models.IntegerField(blank=False, default=0)
    reply = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'notice'

class Comment(models.Model):
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User, on_delete=models.CASCADE,to_field='username', verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    #post = models.ForeignKey(Notice, on_delete=models.CASCADE,to_field='id', verbose_name="댓글")
    report = models.BooleanField(default=False)
    recommend = models.IntegerField(blank=False, default=0)

    class Meta:
        abstract = True

class Noticomment(Comment):
    post = models.ForeignKey(Notice, on_delete=models.CASCADE,to_field='id', verbose_name="댓글")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='parent_comments', null=True)

    class Meta:
        db_table = 'noticomment'

class Rules(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    view = models.IntegerField(blank=False, default=0)
    reply = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'rules'

class Talk(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    view = models.IntegerField(blank=False, default=0)
    report = models.BooleanField(default=False)
    recommend = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'talk'

class Diary(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    view = models.IntegerField(blank=False, default=0)
    report = models.BooleanField(default=False)
    recommend = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'diary'

class Woe(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    view = models.IntegerField(blank=False, default=0)
    report = models.BooleanField(default=False)
    recommend = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'woe'

class Sex(models.Model):
    title       = models.CharField(max_length=200, verbose_name="제목")
    contents    = models.TextField(verbose_name="내용")
    writer      = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE, verbose_name="작성자")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    view = models.IntegerField(blank=False, default=0)
    report = models.BooleanField(default=False)
    recommend = models.IntegerField(blank=False, default=0)
