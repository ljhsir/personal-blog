from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumsExpandMethod, ReadDetail
# Create your models here.

class BlogType(models.Model):  #博客类型
    type_name = models.CharField(max_length=30)

    def __str__(self):
        return '%s' % self.type_name


class Blog(models.Model, ReadNumsExpandMethod):  # 博文
    title = models.CharField(max_length=50)
    read_nums = models.IntegerField(default=0)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    read_detail = GenericRelation(ReadDetail)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.TimeField(auto_now=True)

    def get_email(self):
        return self.author.email

    def get_url(self): 
       return reverse('blog_detail', kwargs={'blog_id':self.id})

    def __str__(self):
        return '%s' % self.title

    class Meta:
        ordering = ['-created_time']







