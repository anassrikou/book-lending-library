from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
# Create your models here.

class Visitor(models.Model):
	"""docstring for Visitor"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cin = models.IntegerField(null=True, blank=True)
	
	def __str__(self):
		return str(self.cin)

	def __unicode__(self):
		return str(self.cin)

	def get_absolute_url(self):
		return reverse("users:profile", kwargs={"id" : self.id})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Visitor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.visitor.save()