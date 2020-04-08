from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from django.dispatch import receiver
# Create your models here.

class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    desc=models.CharField(max_length=300)
    catrgory=models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="review/images",default="")
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    favs =  models.ManyToManyField(User,related_name='favs',blank=True)
    
    def __str__(self):
        return self.product_name

    
    def total_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse("detailproduct",args=[self.id])
    

@receiver(pre_save, sender=Product)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].product_name)
    kwargs['instance'].slug = slug

    


