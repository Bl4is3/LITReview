from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField()
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (300, 300)

    def __str__(self):        
        return (f"Ticket de  {self.user} intitulé {self.title}")
      
    def resize_image(self):
        """ Redimenssionne l  image selon le format défini en constante"""
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """ Surcharge la méthode save avec la redimmension d  image"""
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField( default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="detail")
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="followed_by", blank=True
    )

    class Meta:
        unique_together = ("user","followed_user",)