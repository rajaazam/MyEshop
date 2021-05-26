from django.contrib import admin
from django.urls import path
from.import views
from.middlewares.auth import auth_middleware
#from django.utils.decorators import method_decorator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name='Homepage'),
    path('signup',views.signup,name='singup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout'),
    path('orders',auth_middleware(views.OrderView),name='order'),

]