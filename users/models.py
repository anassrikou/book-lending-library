from django.db import models

# Create your models here.
class Employe(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	phone = models.IntegerField()
	email = models.CharField(max_length=200)
	adress = models.CharField(max_length=200)

	def __str__(self):
		return '%s %s' %(self.first_name, self.last_name)

class Visitor(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	phone = models.IntegerField()
	email = models.CharField(max_length=200)
	CIN = models.IntegerField(unique=True)

	def __str__(self):
		return '%s %s' %(self.first_name, self.last_name)