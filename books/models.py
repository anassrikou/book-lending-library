from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.conf import settings
import datetime
from django.shortcuts import get_object_or_404 
# Create your models here.

ALLOWED_IMG_TYPE = ['png', 'jpg', 'bmp']


class Tags(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Tags"


class Book(models.Model):
	book_name = models.CharField(max_length=200)
	slug = models.CharField(max_length=255, unique=True)
	author_name = models.CharField(max_length=200)
	isbn = models.IntegerField(verbose_name='ISBN', unique=True)
	status = models.BooleanField(default=True)
	description = models.TextField(null=True, blank=True)
	tags = models.ManyToManyField(Tags, blank=True)
	image = models.ImageField(
			null=True, 
			blank=True, 
			width_field="width_field", 
			height_field="height_field")	
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	created = models.DateField(auto_now_add=True)
	number_of_pages = models.IntegerField()
	publish_date = models.DateField()
	publish_place = models.CharField(max_length=200)
	edition = models.CharField(max_length=100)
	borrower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books', blank=True, null=True)


	def __str__(self):
		return self.book_name

	def __unicode__(self):
		return self.book_name

	def get_tags(self):
		tags = ','.join([tag.name for tag in self.tags.all()])
		return tags

	def get_absolute_url(self):
		return reverse("books:detail", kwargs={"id" : self.id})


def create_slug(instance, new_slug=None):
	book_name_lowered = instance.book_name.lower()
	slug = slugify(book_name_lowered)
	if new_slug is not None:
		slug = new_slug
	qs = Book.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def create_image_name(instance):
	# print(instance.image.name)
	image_name = instance.image.name[:-4]
	counter = len(image_name) - 3
	image_ext = instance.image.name[counter:]
	print(image_ext)
	instance.image.name = "%s_img.%s" %(instance.slug, image_ext)
	return instance.image


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
	if instance.image:
		book_name = instance.book_name.lower()
		if not instance.image.name == "%s_img.jpg" %(book_name):
			instance.image = create_image_name(instance)


pre_save.connect(pre_save_post_receiver, sender=Book)


class BookBorrow(models.Model):
	date_borrow_start = models.DateField()
	date_borrow_end = models.DateField(blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	note = models.TextField(blank=True, null=True)
	book_borrowed = models.ForeignKey(Book)

	def __str__(self):
		return str(self.date_borrow_start)

	def __unicode__(self):
		return self.date_borrow_start


def post_save_post_receiver(sender, instance, *args, **kwargs):
	book_id = instance.book_borrowed.id
	book = get_object_or_404(Book, id=book_id)
	book.status = False
	book.borrower = instance.user
	book.save()

post_save.connect(post_save_post_receiver, sender=BookBorrow)


class BookSuggestion(models.Model):
	book_name = models.CharField(max_length=200)
	isbn = models.IntegerField(blank=True, null=True)
	author_name = models.CharField(max_length=200, blank=True, null=True)
	comment = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.book_name

	def __unicode__(self):
		return self.book_name

	