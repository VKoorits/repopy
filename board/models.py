from django.db import models
from django.utils import timezone

class Task(models.Model):
	category = models.CharField(max_length=20)
	task_name = models.CharField(max_length=50)
	description = models.TextField()
	#время закрытия задания
	close_date = models.DateTimeField(default=timezone.now)
	price = models.IntegerField()
	flag = models.CharField(max_length=50)
	
	def __str__(self):
		return self.task_name

class Decision(models.Model):
	user_id = models.IntegerField()
	task_id = models.IntegerField()
	
	def __str__(self):
		return str(user_id) + " -> " + str(task_id)
