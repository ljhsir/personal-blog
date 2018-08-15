from django.shortcuts import render, render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from .models import BlogType, Blog
# Create your views here.
def get_blog_list_common_data(request, all_blogs):
    page_num = request.GET.get('page', 1)  # 获取url的页面参数，（GET请求）
    paginator = Paginator(all_blogs, settings.BLOG_NUM_OF_EACH_PAGE)  # 每10页进行分页
    pages_of_blogs = paginator.get_page(page_num)
    current_page_num = pages_of_blogs.number  # 获取当前页
    page_range = list(range(max(current_page_num - 3, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 3, paginator.num_pages) + 1))

    # 加上省略
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 时间分类的数量
    blog_dates_dict = {}
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')  # 返回一个查询 降序排列
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['page_range'] = page_range
    context['blogs'] = pages_of_blogs.object_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # annotate相当于增加解释，给BlogType增加了一个blog_count属性
    context['pages_of_blogs'] = pages_of_blogs
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    all_blogs = Blog.objects.all()
    context = get_blog_list_common_data(request, all_blogs)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_id, parent=None)
    
    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['comments'] = comments.order_by('-comment_time')
    response = render(request, 'blog/blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true', max_age=180)  # max_age设置cookie最大存活时间为三分钟
    return response
    
def blogs_with_type(request, blog_type_id):
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    all_blogs = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, all_blogs)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    all_blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, all_blogs)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)
