from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from  .models import ReviewRating,product,variation,ProductGallery
from .forms import  *
from category.models import category
from cartapp.models import cartitem
from cartapp.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib import messages
from orders.models import orderproduct

# Create your views here.

def store_page(request,category_slug=None):
    cat=None
    pro=None
    if category_slug !=None:
        cat=get_object_or_404(category,slug=category_slug)
        pro=product.objects.filter(category=cat,is_available=True)
        paginator = Paginator(pro, 1)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page, )
        product_count=pro.count()
    else:

        pro = product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(pro,3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page,)
        product_count=pro.count()
    return  render(request,'store/store.html',{'pro':paged_product,'product_count':product_count,})

def product_details(request,category_slug,product_slug):
    orderpro=None
    try:
        single_product=product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    try:
        orderpro = orderproduct.objects.filter(user=request.user,product_id=single_product.id).exists()

    except :
        pass
    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)

    product_gallery= ProductGallery.objects.filter(product_id=single_product.id)

    return render(request,'store/product_details.html',{'single_product':single_product,'in_cart':in_cart,'orderpro':orderpro,'reviews':reviews,'product_gallery':product_gallery})


def search(request):
    pro=None
    product_count=None
    if 'q' in request.GET:
        keyword=request.GET['q']
        if keyword:
            pro = product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword))
            product_count = pro.count()
    return render(request,'store/store.html',{'pro':pro,'products_count':product_count})


def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method=="POST":
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = Reviewform(request.POST,instance=reviews)
            form.save()
            messages.success(request,'thank you your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form =Reviewform(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success('review has been submit')
                return redirect(url)


