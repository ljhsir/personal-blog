from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
# Create your views here.
def update_comment(request):
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	comment_form = CommentForm(request.POST, user= request.user)
	# 评论数据检查

	data = {}
	if comment_form.is_valid():
		comment = Comment()
		comment.user = comment_form.cleaned_data['user']
		comment.text = comment_form.cleaned_data['text']
		comment.content_object = comment_form.cleaned_data['content_object']
		
		parent = comment_form.cleaned_data['parent']
		if not parent is None:
			comment.root = parent.root if not parent.root is None else parent
			comment.parent = parent
			comment.reply_to = parent.user
		comment.save()
		comment.send_mail()

		# 返回数据
		data['status'] = 'SUCCESS'
		data['username'] = comment.user.username
		data['content_type'] = ContentType.objects.get_for_model(comment).model
		data['comment_time']= comment.comment_time.timestamp()
		data['text'] = comment.text
		if not parent is None:
			data['reply_to']=comment.reply_to.username
		else:
			data['reply_to'] = ''
		data['id']=comment.id
		data['root_id']=comment.root.id if not comment.root is None else ''
	else:
		# return render(request,'error.html', {'message':'评论对象不存在！', 'redirect_to':referer})
		data['status'] = 'ERROR'
		data['message'] = list(comment_form.errors.values())[0][0]
	return JsonResponse(data)