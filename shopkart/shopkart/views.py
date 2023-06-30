from django.http import HttpResponse
from django.shortcuts import  render
from store.models import product

def home(request):
    pro = product.objects.all().filter(is_available=True)
    return render(request,'home.html',{'pro':pro})