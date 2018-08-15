from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone
# Create your models here.
class ReadNums(models.Model):
    # 阅读次数类
    read_nums = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 得到对象类型
    object_id = models.PositiveIntegerField()  # 得到对象id
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumsExpandMethod():
    # 阅读次数变化类
    def get_read_nums(self):
        try:
            ct = ContentType.objects.get_for_model(self)  # 通过对象得到对象类型
            readnums = ReadNums.objects.get(content_type=ct, object_id=self.id)  # 传入对象类型和id，得到关联的阅读次数对象并返回
            return readnums.read_nums
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    # 阅读的详细信息
    date = models.DateField(default=timezone.now)
    read_nums = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 得到对象类型
    object_id = models.PositiveIntegerField()  # 得到对象id
    content_object = GenericForeignKey('content_type', 'object_id')

