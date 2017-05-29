from PIL import Image as PImage

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(
          max_length=20,
          unique=True,
          validators=[RegexValidator(
                regex='^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$',
                message='Your username must be between 3-20 characters long, cannot have a _ or . at the beginning or end and cannot have a __ or _. or ._ or .. inside.',
            ),
          ],
          error_messages={
              'unique': ("A user with that username already exists."),
          },
      )
    profile_picture = models.ImageField(height_field="image_height", width_field="image_width", upload_to='profile_pictures/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    # def get_absolute_url(self):
    #     return reverse("user_profile", kwargs={"username": self.username})


    def save(self, *args, **kwargs):
        if not self.profile_picture:
            return super(User, self).save()

        image = PImage.open(self.profile_picture)
        (width, height) = image.size     
        size = ( 100, 100)
        image = image.resize(size, PImage.ANTIALIAS)
        image.save(self.profile_picture.path)
        return super(User, self).save()


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
      if not self.pk:
          self.slug = slugify(self.name)
      super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
      return reverse("category", kwargs={"slug": self.slug})


    def __str__(self):
        return self.name


class Word(models.Model):
    name = models.CharField(max_length=140)
    definition = models.CharField(max_length=500)
    published = models.DateTimeField(auto_now_add=True, verbose_name=(u'Created'))
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(editable=False)
    # category = models.CharField(max_length=40, default="None", blank=True)
    category = models.ForeignKey(Category)

    def save(self, *args, **kwargs):
        print(self.name)
        print(self.id)
        print(self.user_creator)
        if not self.pk:
            self.slug = slugify(self.name)
        
        print(self.slug)

        super(Word, self).save()

    def get_absolute_url(self):
      return reverse("word_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name



