from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def categories(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'categories.html',context)

def products(request,i):
    c = Category.objects.get(id=i)
    p=Product.objects.filter(category=c)
    context={'cat':c,'pro':p}
    return render(request, 'products.html',context)

def productdetail(request,i):
    p = Product.objects.get(id=i)
    context = {'pro': p}
    return render(request, 'detail.html', context)

def register(request):
    if(request.method=="POST"):
        u=request.POST["u"]
        p = request.POST["p"]
        e = request.POST["e"]
        cp = request.POST["cp"]
        f = request.POST["f"]
        l = request.POST["l"]
        if(p==cp):
            u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            u.save()
        else:
            return HttpResponse("Passwords should be same")

        return redirect('shop:category')
    return render(request,'register.html')
def add_categories(request):
    if (request.method == "POST"):
        n = request.POST['n']
        d = request.POST['d']
        i = request.FILES['i']
        c = Category.objects.create(name=n, desc=d, image=i)
        c.save()
        return redirect('shop:category')
    return render(request, 'addcategories.html')
def add_products(request):
    if (request.method == "POST"):
        n = request.POST['n']
        d = request.POST['d']
        i = request.FILES['i']
        p= request.POST['p']
        s= request.POST['s']
        c= request.POST['c'] #category name
        cat = Category.objects.get(name=c) #retrieves a category record matching with that name
        pro = Product.objects.create(name=n, desc=d, image=i,price=p,stock=s,category=cat) #here category is foreign key field
        pro.save()
        return redirect('shop:category')
    return render(request, 'addproducts.html')
def addstock(request,i):
    p= Product.objects.get(id=i)
    if (request.method == "POST"):  # After submitting the form
        p.stock = request.POST['s']
        p.save()
        return redirect('shop:detail',i)
    context = {'pro': p}
    return render(request, 'addstock.html', context)



def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p) #checks whether the entered details by the user is correct or not
        if user:  #if user record already exists
            login(request,user)
            return redirect('shop:category')
        else: #if user record does not exist
            return HttpResponse("invalid credentials")
    return render(request,'login.html')
def user_logout(request):
    logout(request)
    return redirect('shop:login')
