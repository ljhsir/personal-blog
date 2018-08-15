import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_detail__date__lt=today, read_detail__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_nums_sum=Sum('read_detail__read_nums')) \
                .order_by('-read_nums_sum')
    return blogs[:5]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, seven_days_read_nums = get_seven_days_read_data(blog_content_type)

    # 一周热门博客的缓存
    seven_days_hot_blog = cache.get('seven_days_hot_blog')
    if seven_days_hot_blog is None:
        seven_days_hot_blog = get_7_days_hot_blogs()
        cache.set('seven_days_hot_blog', get_7_days_hot_blogs, 3600)
        print('jisuan')
    else:
        print('use cache')

    context = {}
    context['dates'] = dates
    context['seven_days_read_nums'] = seven_days_read_nums
    context['today_hot_blogs'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_blogs'] = get_yesterday_hot_data(blog_content_type)
    context['week_hot_blogs'] = seven_days_hot_blog

    return render(request, 'home.html', context)
