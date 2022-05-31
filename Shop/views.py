from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Order, OrderItem, Adress, Message
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone
from PayTm import PaytmChecksum
from django.core.exceptions import ObjectDoesNotExist

MERCHANT_KEY = 'kbzk1DSbJiV_03p5'
# Create your views here.
def index(request):
    
    products = Product.objects.all()
    return render(request,'index.html', {'products': products})

   

def accounts(request,):
    if request.method=='POST' :
        if "register" in request.POST:  
         
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password1 = request.POST['password1']
     
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken ')
     
                    return redirect('/Accounts')
                elif User.objects.filter(email = email).exists():
                     messages.info(request, 'Email Taken')
                     return redirect('/Accounts')
                else:
                     new_account = User.objects.create_user(username=username,email=email,password=password)
                     new_account.save()
                     messages.info(request, 'User Created ')
                     print('User created')
         
            else:
                messages.info(request,"Passwords doesn't Match")
                return redirect('/Accounts')   

        elif "login" in request.POST:

            username = request.POST['username']
            password = request.POST['password']
         
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect('/Products')
            else:
                messages.error(request, 'User Not Found')
                return redirect('/Accounts')    

    return render(request, 'account.html')

def logout(request):
     auth.logout(request)
     return redirect('/Accounts')

def products(request):

    products = Product.objects.all()

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    
    products = paginator.get_page(page)

    return render(request, 'products.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        user = request.user
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        text = request.POST['text']

        msg = Message(user=user,full_name=full_name,
        email=email,phone=phone,text=text)
        msg.save()
        return redirect('/ContactUs')

    return render(request, 'contact.html')

@login_required(login_url="/Accounts")
def cart(request):
    order = Order.objects.filter(user= request.user)
    cart_items = OrderItem.objects.filter(user = request.user)
    context ={
        'cart_items': cart_items,
        'order': order
    }
    
    return render(request, 'cart.html', context)

def product(request, product_slug):
    product = Product.objects.filter(slug=product_slug)

    return render(request, 'productview.html', {'product':product[0]})

@login_required(login_url="/Accounts")
def add_to_cart(request, product_slug):
    item = get_object_or_404(Product, slug=product_slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user= request.user,ordered=False)
    order_qs = Order.objects.filter(user = request.user, ordered= False)

    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()

        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now() 
        order = Order.objects.create(user= request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('/Cart')   


@login_required(login_url="/Accounts")   
def remove_from_cart(request, product_slug):
    item = get_object_or_404(Product, slug=product_slug)
    order_qs = Order.objects.filter(user = request.user, ordered= False)

    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user= request.user,ordered=False)[0]
            order.items.remove(order_item) 
            order_item.delete()  
            return redirect('/Cart')

        else:
            #add a msg,no order item
            return redirect('/Cart')  
            
    else:
        #add a msg,no order
        return redirect('/Cart')     
       
    return render(request, 'cart.html')         


@login_required(login_url="/Accounts")
def decrease_quantity(request, product_slug):
    item = get_object_or_404(Product, slug=product_slug)
    order_qs = Order.objects.filter(user = request.user, ordered= False)

    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
               order_item = OrderItem.objects.filter(item=item, user= request.user,ordered=False)[0]
               if order_item.quantity > 1:
                  order_item.quantity -=1
                  order_item.save()
                  return redirect('/Cart')
               else:
                    order.items.remove(order_item) 
                    order_item.delete() 
                    return redirect('/Cart')

        else:
            #add a msg,no order item
            return redirect('/Cart')  
            
    else:
        #add a msg,no order
        return redirect('/Cart')     
       
    return render(request, 'cart.html')         


@login_required(login_url="/Accounts")
def checkout(request):

    if request.method=='POST':
        try:    
          order = Order.objects.get(user = request.user, ordered= False)

          user = request.user
          full_name = request.POST['full_name']
          adress = request.POST['adress']
          email = request.POST['email']
          amount = request.POST['amount']
          state = request.POST['state']
          pin_code = request.POST['pin_code']
          contact = request.POST['contact']
          payment_c = request.POST['payment_c']
  
          new_adress = Adress(user=user, full_name=full_name,
          first_adress = adress, email= email, state=state,
          pin_code=pin_code,contact=contact)
          
          new_adress.save()
          order.adress = new_adress
          order.total_amount = amount
          order.save()
          
          param_dict = {
              'MID' : '',
              'ORDER_ID' : str(order.order_id),
              'TXN_AMOUNT' : str(amount),
              'CUST_ID' : email,
              'INDUSTRY_TYPE_ID' : 'Retail',
              'WEBSITE' : 'WEBSTAGING',
              'CHANNEL_ID' : 'WEB',
              'CALLBACK_URL' : 'http://127.0.0.1:8000/handlerequest',
          }
          param_dict['CHECKSUMHASH'] = PaytmChecksum.generateSignature(param_dict, MERCHANT_KEY)
          return render(request, 'paytm.html', {'param_dict':param_dict})
  
        except ObjectDoesNotExist:
            return redirect('/Checkout')
       
    order = Order.objects.filter(user= request.user)
    cart_items = OrderItem.objects.filter(user = request.user)
    data = {
        'cart_items': cart_items,
        'order': order
    }
    return render(request,'checkout.html', data)

@csrf_exempt
def handlerequest(request):
    #Paytm send post request
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]= form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify =  Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Congratulations! Order successful')
        else:
            print('Payment Failed,' + response_dict['RESPMSG'])           
    return render(request, 'handle.html', {'response': response_dict })
   