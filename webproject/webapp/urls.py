from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin',views.adminhome,name='adminhome'),
    path('signup/', views.MySignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout',views.LogoutView.as_view(), name='logout'),

    path('cart_view/', views.cart_view, name='cart_view'),
    path('addcart/<int:product_id>/', views.add_to_cart, name='addcart'),
    path('cart/update/<int:item_id>/',views.update_cart, name='update_cart'),
    path('cart/delete/<int:item_id>/',views.delete_cart, name='delete_cart'),

    path('profile',views.profile,name='profile'),
    path('productview', views.productview, name='productview'), 
    path('order_view/',views.order_view, name='order_view'),
    path('address/<int:order_id>',views.address,name='address'),
    path('proced_order/<int:order_id>',views.proced_order,name='proced_order'),
    path('totalorder',views.totalorder,name='totalorder'),

    path('addproduct_adm',views.addproduct_adm,name='addproduct_adm'),
    path('viewproduct_adm',views.viewproduct_adm,name='viewproduct_adm'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('update/<int:product_id>/', views.product_update, name='product_update'),
    path('remove/<int:product_id>/', views.product_delete, name='product_delete'),
    path('customers/',views.customers,name='customers'),
    path('orderlists/',views.total_orders,name='total_orders')
    
]














