import threading
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.loader import render_to_string
# Create your models here.

class SendMail(threading.Thread):
    def __init__(self, title, text, email):
        self.text = text
        self.email = email
        self.host = settings.EMAIL_HOST_USER
        threading.Thread.__init__(self)

    def run(self):
        send_mail('','', self.host, [self.email],  fail_silently = False, html_message = self.text)

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 得到对象类型
    object_id = models.PositiveIntegerField()  # 得到对象id
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)  # 用related_name可以反向找到自己的评论

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def send_mail(self):
        if self.parent is None:
            # 评论了你的博客
            title = '有人对你发布的内容进行了评论：'
            email = self.content_object.get_email()
        else:
            #回复了你的评论
            title = '有人回复了你的评论：'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['title']=title
            context['messages'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_message.html', context)
            send_email = SendMail(title, text, email)
            send_email.start()

    def __str__(self):
    	return self.text

    class Meta:
    	ordering=['comment_time',]