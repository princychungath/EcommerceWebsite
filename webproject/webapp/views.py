from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from .forms import ProductForm,OrderForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView
from .models import Product,Cart,CartItem,Order,OrderItems
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def home(request):
    return render(request,'webapp/base.html')
  
class MySignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'webapp/signup.html'
    success_url = reverse_lazy('login')

@login_required    
class MyLogoutView(LogoutView):
    pass

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'webapp/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('adminhome')
                else:
                    return redirect('home')
        context = {'form': form}
        return render(request, 'webapp/login.html', context)

@login_required
def adminhome(request):
    return render(request,'webapp/adminhome.html')


@login_required
def productview(request):
    products = Product.objects.all()
    return render(request, 'webapp/productlist.html', {'products': products})


@login_required
def profile(request):
    return render(request,'webapp/profile.html')


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'webapp/product_details.html', {'product': product})


@login_required
def add_to_cart(request,product_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(user=user)
    try:
        cart_item = CartItem.objects.get(cart=cart,product=product)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart,product=product,quantity=1)
    return redirect('cart_view')


@login_required
def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    context = {
        'user': user,
        'cart_items': cart_items  
    }
    return render(request, 'webapp/cart.html', context)

@login_required
def delete_cart(request,item_id):
  cart_item= get_object_or_404(CartItem, id=item_id)
  cart_item.delete()
  return redirect("cart_view")


@login_required  
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity'))

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_view')


@login_required
def order_view(request):
    user = request.user
    cart = user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    print("Total Price:", total_price)
    order = Order.objects.create(user=user, total_price=total_price)
    for cart_item in cart_items:
        product = cart_item.product
        quantity_to_buy = cart_item.quantity
        
        if product.quantity >= quantity_to_buy:
            product.quantity -= quantity_to_buy
            product.save()
            OrderItems.objects.create(order=order, product=product, quantity=quantity_to_buy)
    
    cart_items.delete()
    order_items = OrderItems.objects.filter(order=order)
    request.session['order_id'] = order.id
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'webapp/order.html', context)


@login_required
def address(request, order_id):
    order= get_object_or_404(Order, id=order_id) 
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            payment_method = form.cleaned_data['payment_method']
    else:
        form = OrderForm()
    return render(request, 'webapp/address.html', {'form': form, 'order_id': order_id})


@login_required
def proced_order(request, order_id):
    order= get_object_or_404(Order, id=order_id) 
    context = {
        'order': order,
    }
    return render(request, 'webapp/orderconf.html', context)


@login_required
def totalorder(request):
    order_items = OrderItems.objects.all()
    context = {'order_items': order_items}
    return render(request, 'webapp/orderlists.html', context)


@login_required
def addproduct_adm(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']

            if price >= 1 and quantity >= 1:
                form.save()
                return redirect('viewproduct_adm')
            else:
                form.add_error(None, "Price and quantity must be greater than or equal to 1.")
    else:
        form = ProductForm()

    return render(request, 'webapp/admin_addproduct.html', {'form': form})



@login_required   
def viewproduct_adm(request):
    products = Product.objects.all()
    return render(request, 'webapp/viewproduct_adm.html', {'products': products})


@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('viewproduct_adm')
    else:
        form = ProductForm(instance=product)
    return render(request, 'webapp/update.html', {'form': form})


@login_required
def product_delete(request,product_id):
  product= get_object_or_404(Product, id=product_id)
  product.delete()
  return redirect("viewproduct_adm")


@login_required
def customers(request):
    customers =User.objects.all()
    return render(request,'webapp/customers.html', {'customers': customers})

@login_required
def total_orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'webapp/total_orders.html', context)





