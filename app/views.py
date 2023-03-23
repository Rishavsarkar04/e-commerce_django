from django.shortcuts import render ,redirect
from django.views import View
from .models import Product,Cart,Customer,OrderPlaced,Payment
from .form import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        search = request.GET.get('search')
        exist =False
        if 'search' in request.GET and search !='':
            s = Product.objects.filter(title__contains=search)
            exist =True
            context = { 
                    'search_product': s,
                    'exist':exist,
                    'search':search,
            }
        elif 'search' not in request.GET or search =='':
            topwear = Product.objects.filter(category='TW')
            mobile = Product.objects.filter(category='M')
            laptop = Product.objects.filter(category='L')
            bottomwear = Product.objects.filter(category='BW')

            context = { 'topwears':topwear,
                        'mobiles':mobile,
                        'laptops':laptop,
                        'bottomwears':bottomwear,
            }
        return render(request, 'app/home.html', context)

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product =Product.objects.get(pk=pk)
        user = request.user
        exist = False
        if user.is_authenticated:
            cart = Cart.objects.filter(user=user,product=product)  
            if cart.exists():
                exist=True
        real_price = product.selling_price - product.discounted_price
        percentage =  int((product.discounted_price/product.selling_price)*100)
        context = {
            'product':product,
            'real_price':real_price,
            'percentage':percentage,
            'exist':exist,
        }
        return render(request, 'app/productdetail.html', context)


@login_required
def adjust_cart(request):
    user = request.user
    if 'plus' in request.POST:
        prod_id = request.POST.get('plus').split('-')[1]
        product = Product.objects.get(id=prod_id) 
        c = Cart.objects.get(product=product , user = user)
        c.quantity = c.quantity + 1
        c.save()
    elif 'minus' in request.POST:
        prod_id = request.POST.get('minus').split('-')[1]
        product = Product.objects.get(id=prod_id) 
        c = Cart.objects.get(product=product , user = user)
        if c.quantity == 1:
            c.delete()
        else:
            c.quantity = c.quantity - 1
            c.save()
    elif 'remove' in request.POST:
        prod_id = request.POST.get('remove').split('-')[1]
        product = Product.objects.get(id=prod_id) 
        c = Cart.objects.get(product=product , user = user)
        c.delete()     
    return redirect('show_cart')
        
def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
   def get(self,request):
      form = CustomerProfileForm()
      return render(request, 'app/profile.html', {'form':form , 'active':'btn-primary'})
   def post(self,request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
        object = form.save(commit=False)
        object.user = request.user
        object.save()
        messages.success(request, 'congratulations !! new profile created successfully' )
      return render(request, 'app/profile.html', {'form':form,'active':'btn-primary'})

@login_required
def address(request):
    add = Customer.objects.filter(user = request.user).all()
    exist = False
    if add.exists():
        exist = True
    return render(request, 'app/address.html',{'addresses': add ,'active':'btn-primary', 'exist': exist})

@login_required
def edit_add(request,id):
    cus = Customer.objects.get(id=id)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST,instance=cus)
        form.save()
        messages.success(request, 'congratulations !! profile have been updated successfully' )
    else:
        form = CustomerProfileForm(instance=cus)
    
    return render(request, 'app/edit_add.html', {'form':form,'active':'btn-primary'})
    
@login_required
def delete_add(request,id):
    cus = Customer.objects.get(id=id)
    cus.delete()
    return redirect('address')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data = None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
        cat=Product.objects.filter(category='M').values_list('brand', flat=True).distinct()
        context = {
            'mobiles': mobiles,
            'category': cat,
        }
    else:
        mobiles = Product.objects.filter(category='M').filter(brand=data)
        cat = Product.objects.filter(category='M').values_list('brand', flat=True).distinct()
        context = {
            'mobiles': mobiles,
            'category': cat
        }
    return render(request, 'app/mobile.html', context)

def topwear(request, data = None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
        cat=Product.objects.filter(category='TW').values_list('brand', flat=True).distinct()
        context = {
            'topwears': topwears,
            'category': cat,
        }
    else:
        topwears = Product.objects.filter(category='TW').filter(brand=data)
        cat = Product.objects.filter(category='TW').values_list('brand', flat=True).distinct()
        context = {
            'topwears': topwears,
            'category': cat
        }
    return render(request, 'app/topwear.html', context)


def bottomwear(request, data = None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
        cat=Product.objects.filter(category='BW').values_list('brand', flat=True).distinct()
        context = {
            'bottomwears': bottomwears,
            'category': cat,
        }
    else:
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
        cat = Product.objects.filter(category='BW').values_list('brand', flat=True).distinct()
        context = {
            'bottomwears': bottomwears,
            'category': cat
        }
    return render(request, 'app/bottomwear.html', context)

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
      form = CustomerRegistrationForm()
      return render(request, 'app/customerregistration.html', {'form':form})      
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'congratulations !! registration successfully done' )
        return render(request, 'app/customerregistration.html', {'form':form})  

@login_required
def add_to_cart(request):
    prod_id = request.POST.get('prod-id')
    product = Product.objects.get(id=prod_id) 
    user = request.user
    a = Cart(user= user,product=product)
    a.save()
    return redirect('/cart')

@login_required
def show_cart(request):
   if request.user.is_authenticated:
        user =request.user
        cart = Cart.objects.filter(user= user).all()
        amount = 0.0
        shipment_amount= 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user ]
        cart_empty = 'false'
        if cart_product:
            for p in cart_product:
                tem_amount = (p.product.selling_price - p.product.discounted_price)*p.quantity
                amount = amount + tem_amount
            total_amount = amount + shipment_amount
        else:
           cart_empty = 'true'
        return render(request, 'app/addtocart.html',{'carts':cart , 'total_amount' : total_amount , 'shipment_amount' : shipment_amount , 'amount':amount,'cart_empty':cart_empty})


@csrf_exempt
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    print(add)
    buy_now = request.GET.get('buynow')
    prod_id = request.GET.get('prod-id')
    amount = 0.0
    shipment_amount= 70.0
    total_amount = 0.0
    one_item=False
    if buy_now=='yes':
        product_id = Product.objects.get(id=prod_id) 
        user = request.user
        a = Cart(user= user,product=product_id)
        a.save()
        items = Cart.objects.get(user=user,product=product_id)
        amount=items.total_cost
        one_item=True
    else:
        items = Cart.objects.filter(user=user).all()
        cart_product = [p for p in Cart.objects.all() if p.user == user ]
        for p in cart_product:
            tem_amount = (p.product.selling_price - p.product.discounted_price)*p.quantity
            amount = amount + tem_amount

    total_amount = amount + shipment_amount

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET ))
    payment_response=client.order.create({
    "amount" : total_amount*100,
    "currency" : "INR"
    })
    order_id=payment_response['id']
    context={
        'addresses': add,
        'items': items ,
         'total_amount' : total_amount ,
           'shipment_amount' : shipment_amount ,
           'amount':amount,
           'pay_payment':total_amount*100,
           'order_id': order_id,
           'one_item': one_item,
    }
    return render(request, 'app/checkout.html',context=context)
    

@login_required
def payment_done(request):
    cus_id = request.GET.get('cusid')
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    signature = request.GET.get('signature')
    user = request.user

    if cus_id == '':
        messages.info(request, 'please select a address')
        return redirect('checkout')
    else:
        payment = Payment(user=user, razorpay_order_id=order_id, razorpay_payment_id=payment_id, razorpay_signature_id=signature, paid=True)
        payment.save()
        cart = Cart.objects.filter(user=user)
        customer = Customer.objects.get(user=user,id=cus_id)
        print(customer.name)
        for c in cart:
            OrderPlaced(user=user,payment=payment, customer_name=customer.name , locality=customer.locality , city=customer.city , zipcode=customer.zipcode , state=customer.state , product=c.product , quantity=c.quantity  ).save()
            c.delete()
        return redirect('orders')

@login_required
def orders(request):
    user = request.user
    orders = OrderPlaced.objects.filter(user = user)
    exist = False
    if orders.exists():
        exist = True
    return render(request, 'app/orders.html',{'exist': exist, 'orders':orders})
