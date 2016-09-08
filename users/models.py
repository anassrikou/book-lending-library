from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
# Create your models here.

class Visitor(models.Model):
	"""docstring for Visitor"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cin = models.IntegerField()
	
	def __str__(self):
		return self.cin

	def __unicode__(self):
		return self.cin


# def create_cin_after_register(sender, instance, *args, **kwargs):
# 	user = instance
# 	self.user = get_or_create(User)

# pre_save.connect(create_cin_after_register, sender=User)