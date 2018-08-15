import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNums, ReadDetail



def read_statistics_once_read(request, obj):
    # 传入请求和处理对象，检查cookie，如果符合要求，增加一次阅读次数，否则不做任何操作，最后返回对象类型和id
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.id)
    # 阅读数加一
    if not request.COOKIES.get(key):
        readnums, created = ReadNums.objects.get_or_create(content_type=ct, object_id=obj.id)
        readnums.read_nums += 1
        readnums.save()

    # 当天阅读数加一
    date = timezone.now().date()
    if not request.COOKIES.get(key):
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
        readDetail.read_nums += 1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    seven_days_read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%y/%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_detail.aggregate(read_nums_sum=Sum('read_nums'))
        seven_days_read_nums.append(result['read_nums_sum'] or 0)
    return dates, seven_days_read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_nums')
    return read_detail[:5]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_nums')
    return read_detail[:5]

def get_seven_days_hot_data(content_type):
    today = timezone.now().date()
    week = today - datetime.timedelta(days=7)
    read_detail = ReadDetail.objects \
                            .filter(content_type=content_type, date__lt=today, date__gte=week) \
                            .values('content_type', 'object_id') \
                            .annotate(week_read_nums_sum=Sum('read_nums'))\
                            .order_by('-week_read_nums_sum')
    return read_detail[:5]
