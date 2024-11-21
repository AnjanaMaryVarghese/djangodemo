from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart,Payment,Order_details
import razorpay
# Create your views here.
def addtocart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:  #if product is already present inside table for the current user
        c = Cart.objects.get(user=u,product=p)
        c.quantity +=1  #it will increment the quantity inside the record
        p.stock-=1
        p.save()
        c.save()
    except: #if not present
        c = Cart.objects.create(product=p, user=u, quantity=1) #it will add a new record with quantity =1
        p.stock -= 1
        p.save()
        c.save()

    return redirect('cart:cartview')

def cartview(request):
    u=request.user
    c=Cart.objects.filter(user=u) #to filter cart records for a particular user
    total=0
    for i in c:
        total += i.quantity * i.product.price
    context={'cart':c,'total':total}
    return render(request, 'addtocart.html',context)

def cartremove(request,i):
    u=request.user
    p=Product.objects.get(id=i)

    try:
        c=Cart.objects.get(user=u,product=p)
        if (c.quantity > 1 ):
            c.quantity-=1
            c.save()
            p.stock += 1
            p.save()
        else : # if cart quantity =0
            c.delete()
            p.stock+=1
            p.save()
    except:
        pass
    return redirect('cart:cartview')

def cartfullremove(request,i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)
        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')

def orderform(request):
    if request.method=="POST":
        #Read input from the form fields
        a=request.POST['a']
        pn=request.POST['p']
        pi=request.POST['pi']

       #for calculating total bill amount
        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total+=i.product.price*i.quantity
        print(total)
        #Razorpay connection
        client=razorpay.Client(auth=('rzp_test_7MBIFnOwDq442U','XbU6AIC7Oc6rXDOkKH4DUNEG'))
        #Razorpay order creation
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        order_id=response_payment['id'] #retrieve the order id from response
        status=response_payment['status'] #retrieve the status from response
        if(status=='created'):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(product=i.product,user=i.user,address=a,phone=pn,pin=pi,order_id=order_id,no_of_items=i.quantity)
                o.save()
            context={'payment':response_payment,'name':u.username} #sends the response from view to payment.html
            return render(request, 'payment.html',context)
    return render(request, 'placeorder.html')
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
@csrf_exempt
def paymentstatus(request,p):
    user=User.objects.get(username=p) #retrieve user object
    login(request,user)
    response=request.POST
    print(response)

    #to check the validity(authenticity) of razorpay payment details received by application
    param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
        }
    client=razorpay.Client(auth=('rzp_test_7MBIFnOwDq442U','XbU6AIC7Oc6rXDOkKH4DUNEG'))
    try:
        status=client.utility.verify_payment_signature(param_dict) #for checking the payment details
                                                                   #we pass param_dict to verify_payment_signature function
        print(status)
        p=Payment.objects.get(order_id=response['razorpay_order_id']) #after successful payment retrieve the payment record matching with response['order_id']
        p.razorpay_payment_id=response['razorpay_payment_id']   #assigns response [paymentid] to razorpay_payment_id
        p.paid=True
        p.save()

        o=Order_details.objects.filter(order_id=response['razorpay_order_id']) #After successful payment retrieve the order details records matching with response
        print(o)
        for i in o:
            i.payment_status="completed" #assigns "completed" to payment_status in each record
            i.save()
        #to remove cart items for a particular user after successful payment
        c=Cart.objects.filter(user=user)
        print('hello')
        print(c)
        c.delete()
    except:
        pass
    return render(request,'paymentstatus.html')
def orderview(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status='completed')
    context={'orders':o}
    return render(request,'orderview.html',context)

