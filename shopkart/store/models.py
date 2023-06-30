from django.db import models
from category.models import category

# Create your models here.
from django.urls import reverse


class product(models.Model):
    product_name  = models.CharField(max_length=200,unique=True)
    slug          = models.SlugField(max_length=200,unique=True)
    description   = models.TextField(max_length=500,blank=True)
    price         = models.IntegerField()
    images        = models.ImageField(upload_to='photos/product')
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(category,on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])



class variationManager(models.Manager):
    def colors(self):
        return super(variationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(variationManager,self).filter(variation_category='size',is_active=True)

variation_category_chocie=(
    ('color','color'),
    ('size','size')
)

class variation(models.Model):
    product  = models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200,choices=variation_category_chocie)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects=variationManager()


    def __str__(self):
        return self.variation_value