from django.shortcuts import render, redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
#from Eshop.store.middlewares.auth import auth_middleware

from django.contrib.auth.hashers import make_password, check_password
from django.views import  View



# Create your views here.
def Home(request):
    if request.method == 'GET':
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']= {}


        products = None
        categories = Category.get_all_categories();
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products();

        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are :', request.session.get('email'))

        return render(request, 'index.html', data)

    else:
        product = request.POST.get('product')
        remove= request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            qunatity=cart.get(product)
            if qunatity:
                if remove:
                    if qunatity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = qunatity - 1


                else:
                    cart[product] = qunatity + 1


            else:
                cart[product] = 1





        else:
            cart={}
            cart[product] = 1
    request.session['cart']=cart
    print('cart',request.session['cart'])
    return redirect('Homepage')
























def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        postData = request.POST
        firstName = postData.get('firstname')
        lastName = postData.get('lastname')
        email = postData.get('email')
        phone = postData.get('phone')
        password = postData.get('password')

        #validations
        value={
            'firstName':firstName,
            'lastName': lastName,
            'phone': phone,
            'email':email

        }
        error_message = None
        customer = Customer(firstName=firstName,
                            lastName=lastName,
                            email=email,
                            phone=phone,
                            password=password)
        if (not firstName):
            error_message = 'First Name must be required !!'
        elif len(firstName) <= 3:
            error_message = 'First Name must be 3 character long or more !'
        elif not lastName:
            error_message = 'Last Name must be required !!'
        elif len(lastName) <= 3:
            error_message = 'Last Name must be 3 character long or more'
        elif not phone:
            error_message = 'phone number must be required !'
        elif len(phone) <= 10:
            error_message = 'Phone number must be 10 char long'
        elif len(password) <=6:
            error_message = 'Password must be 6 char long'
        elif len(email) <=4:
            error_message = 'Email must be 4 char long'
        elif customer.isExists():
            error_message = 'Email is already register enter new email'




        #save
        if not error_message:
            print(firstName, lastName, email, phone, password)
            customer.password=make_password(customer.password)

            customer.register()
            return redirect('Homepage')

        else:
            data={
                'error':error_message,
                'values':value
            }
            return HttpResponse(request,'signup.htm',data)





def login(request):
    return_url=None
    if request.method == 'GET':
        login.return_url=request.GET.get('return_url')
        return render(request, 'login.html')


    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)

        error_message = None
    if customer:
        flag = check_password(password, customer.password)
        if flag:
            request.session['customer']= customer.id
            #request.session['email']=customer.email
            if login.return_url:
                return HttpResponseRedirect(login.return_url)
            else:
                login.return_url = None
                return redirect('Homepage')

        else:
            error_message = 'Email or password invalid !!'

    else:
        error_message = 'Email or password invalid !!'
        print(email, password)
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')
   #return render(request, 'logout.html')

def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    print(products)
    return render(request, 'cart.html',{'products':products})


def checkout(request):
    if request.method ==' POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)


        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')




def OrderView(request):
    #method_decorator(auth_middleware())
    if request.method == 'GET':
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)

        print(orders)
        orders = orders.reverse()

        return render(request, 'orders.html', {'orders': orders})













