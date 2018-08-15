from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nickname = models.CharField(max_length=30)

	def __str__(self):
		return "<Profile:%s for %s>"%(self.nickname, self.user)

def get_nickname_or_username(self):
	if Profile.objects.filter(user=self).exists():
		profile = Profile.objects.get(user=self)
		return profile.nickname
	else:
		return self.username
# 给User动态添加一个方法
User.get_nickname_or_username=get_nickname_or_username