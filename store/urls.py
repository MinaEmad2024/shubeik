from django.urls import path 
from .import views



urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('register/',views.register_user, name='register'),
    path('update_password/',views.update_password, name='update_password'),
    path('update_user/',views.update_user, name='update_user'),
    path('update_info/',views.update_info, name='update_info'),
    path('product/<int:pk>',views.product, name='product'),
    path('category/<str:foo>',views.category, name='category'),
    path('category_summary/',views.category_summary, name='category_summary'),
    path('add_new_product/<int:id>',views.add_new_product, name='add_new_product'),
    path('edit_product/<int:id>',views.edit_product, name='edit_product'),
    path('add_new_shop/',views.add_new_shop, name='add_new_shop'),
    path('my_shop/<int:id>',views.my_shop, name='my_shop'),
    path('view_shop/<int:id>',views.view_shop, name='view_shop'),
    path('view_shop_generic/<int:id>',views.view_shop_generic, name='view_shop_generic'),
    path('search/',views.search, name='search'),

] 