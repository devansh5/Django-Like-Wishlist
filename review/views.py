from django.shortcuts import render , redirect,get_object_or_404,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
# Create your views here.
from review.models import Product
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login ,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

# from math import ceil

def index(request):
    products=Product.objects.all()
    paginator=Paginator(products,9)
    page=request.GET.get('page')
    products=paginator.get_page(page)
    params={'products':products}
    return render(request,'index.html',params)

def detail(request,pk):
    product=Product.objects.get(pk=pk)
    is_fav=False
    is_liked=False
    if product.likes.filter(id=request.user.id).exists():
        is_liked=True
    if product.favs.filter(id=request.user.id).exists():
        is_fav=True
    context={'product':product,'is_liked':is_liked,'is_fav':is_fav,'total_likes':product.total_likes()}
    return render(request,'test.html',context)


def about(request):
    return render(request,'review/about.html')

def contact(request):
    return render(request,'we are contact')

def tracker(request):
    return render(request,'we track order')

def search(request):
    return render(request,'we are search')

def prodView(request):
    return render(request,'we are prodView')

def checkout(request):
    return render(request,'we are checkout')

def handlesignup(request):
    if request.method == 'POST':
         username = request.POST['username']
         email = request.POST['email']
         phone = request.POST['phone']
         pass1 = request.POST['pass1']
         pass2 = request.POST['pass2']

         myuser = User.objects.create_user(username ,email , pass1)
         myuser.Phone = phone
         myuser.save()
         messages.success(request,"your account successfully created")
         return redirect('/')
    else:
         return Httpresponse('Not allowed')

def handlelogin(request):
      if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        
        User =  authenticate(username =loginusername, password = loginpassword)
    
        if User is not None:
            login(request,User)
             
            return redirect('/') 
        else :
             messages.error(request,"Invalid Credentials")
             return redirect('/')
      return HttpResponse('handlelogin')

def handlelogout(request):
     logout(request)
     return redirect('/')

def like(request):
    # product=get_object_or_404(Product,id=request.POST.get('product_id'))
    product=get_object_or_404(Product,id=request.POST.get('id'))
    
    is_liked=False
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        is_liked=False
    else:
        product.likes.add(request.user)
        is_liked=True
    context={'product':product,'is_liked':is_liked,'total_likes':product.total_likes()}
    if request.is_ajax():
        html=render_to_string('like_section.html',context,request=request)
        return JsonResponse({'form':html})

def fav(request):
    product=get_object_or_404(Product,id=request.POST.get('id'))
    
    is_fav=False
    if product.favs.filter(id=request.user.id).exists():
        product.favs.remove(request.user)
        is_fav=False
    else:
        product.favs.add(request.user)
        is_fav=True
    context={'product':product,'is_fav':is_fav}
    if request.is_ajax():
        html=render_to_string('fav_section.html',context,request=request)
        return JsonResponse({'form':html})
    

def wishlist(request):
    user=request.user
    liked_products=user.favs.all()
    context={
        'liked_products':liked_products
    }
    return render(request,'wishlist.html',context)










