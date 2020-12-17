from django.shortcuts import render,redirect
from .models import Products , Category , Tags, Cart, Cartitems
from .forms import ProductForm,CartItemForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url = 'user_login')
def product_list(request):
    print(request.role)
    product = Products.objects.all()
    return render(request,'product_page.html',{'products':product,})

@login_required(login_url = 'user_login')
def by_category(request):
    category = Category.objects.all()
    return render(request, 'category_page.html', {'categorys':category})

@login_required(login_url = 'user_login')
def add(request):
    add=ProductForm()
    if request.method=='POST':
        add=ProductForm(request.POST,request.FILES)
        if add.is_valid():
            add.save()
            return redirect('all_products')
    else:
        return render(request, 'product_add.html', {'upload_form':add,"title":'Add New Product',})

@login_required(login_url = 'user_login')
def update_prod(request,prod_id):
    print(type(prod_id))
    prod_id=int(prod_id)
    try:
        product=Products.objects.get(id=prod_id)
    except Products.DoesNotExist:
        return redirect('all_products')
    title_string = f"Edit {product.product_name} information"
    prod_edit=ProductForm(request.POST or None, instance=product)
    if prod_edit.is_valid():
        prod_edit.save()
        return redirect('all_products')
    return render(request, 'product_add.html', {'upload_form':prod_edit,"title":title_string,})

@login_required(login_url = 'user_login')
def delete_prod(request,prod_id):
    prod_id=int(prod_id)
    try:
        product=Products.objects.get(id=prod_id)
    except Products.DoesNotExist:
        return redirect('all_products')
    product.delete()
    return redirect('all_products')


@login_required(login_url = 'user_login')
def add_to_cart(request,prod_id):
    prod_id=int(prod_id)
    try:
        product=Products.objects.get(id=prod_id)
    except Products.DoesNotExist:
        return redirect('all_products')
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user = request.user,cart_name=str(request.user))
        cart.save()
    try:
        cart_item=Cartitems.objects.get(prod_id=prod_id,cart_name=str(request.user))
        print(f'##########cart name = {cart_item.cart_name}###########')
        print(f'##########user name = {request.user}###########')
        cart_item.qnty += 1
        cart_item.final_price = cart_item.item_price * cart_item.qnty
        cart_item.save()
        cart.total += cart_item.item_price
        if cart.total > 10000:
            cart.discounted_price = cart.total - 500
        print(f'current item price {cart_item.item_price} and total price {cart.total}')
        cart.save()
    except Cartitems.DoesNotExist:
        cart_item = Cartitems.objects.create(cart = cart,cart_name=str(request.user), item_name = product.product_name, item_price =product.price, final_price=product.price, prod_id= prod_id)
        cart_item.save()
        cart.total += cart_item.item_price
        if cart.total > 10000:
            cart.discounted_price = cart.total - 500
        print(f'current item price {cart_item.item_price} and total price {cart.total}')
        cart.save()
    return redirect('my_cart')

@login_required(login_url = 'user_login')
def cart_list(request):
    print(f'#### {request.user} ####')
    cart = Cart.objects.get(cart_name = str(request.user))
    ct = cart.cartitems_set.all()
    total = 0 
    msg = 'Your cart is empty'
    dis_msg = ''
    discounted_price = 0
    for citem in ct:
        msg = 'have a look at your cart'
        print(citem.final_price)
        total += citem.final_price
    if total > 10000:
        dis_msg = 'Congratulations you are getting 500 RS discount'
        discounted_price = total - 500
    return render(request, 'cart.html', {'cart':cart,'total':total,'msg':msg,'new_price':discounted_price,'dis_msg':dis_msg})

@login_required(login_url = 'user_login')
def remove_from_cart(request,prod_id):
    cart = Cart.objects.get(user = request.user)
    cart_item=Cartitems.objects.get(prod_id=prod_id,cart_name=str(request.user))
    if (cart_item.qnty > 1):
        cart_item.qnty -= 1
        cart_item.final_price = cart_item.item_price * cart_item.qnty
        cart_item.save()
        cart.total -= cart_item.item_price
        if cart.total > 10000:
            cart.discounted_price = cart.total - 500
        print(f'current item price {cart_item.item_price} and total price {cart.total}')
        cart.save()
    else:
        cart_item.delete()
        cart.total -= cart_item.item_price
        if cart.total > 10000:
            cart.discounted_price = cart.total - 500
        print(f'current item price {cart_item.item_price} and total price {cart.total}')
        cart.save()
    return redirect('my_cart')

@login_required(login_url = 'user_login')
def all_carts(request):
    
    cart = Cart.objects.all()
    return render(request, 'all_cart.html',{'cart':cart})