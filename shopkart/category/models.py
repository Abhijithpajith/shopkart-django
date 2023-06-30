from django.db import models

# Create your models here.
from django.urls import reverse


class category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description= models.TextField(max_length=200,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])