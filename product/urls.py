from django.urls import path
from .views import order_to_pdf,home,chage_order_status,home_offer,cart,checkout,updateItem,removeItem,handlepayment,placeOrder,myorder,product_view,buyNow,autocompleteModel,search,myProfile,Changeusername,ProfileUpdateview,like,myWishlist,Contactus,BugreportView

urlpatterns = [
       path('',home,name='home_page'),
       
       path('home_offer/<int:pk>/<str:event>/<slug:slug>/',home_offer,name='home_page_category'),
       path('product_detail/<int:pk>/<slug:slug>/',product_view,name='product_detail'),
              
       path('cart/',cart,name='cart'),
       path('checkout/',checkout,name='checkout'),
       path('update_cart/<int:pk>/<str:event>/',updateItem,name='update_cart'),
       path('buy_now/<int:pk>/<str:event>/',buyNow,name='buy_now'),
       path('remove_item/<int:pk>/',removeItem,name='remove_item'),
       path('place_order/',placeOrder,name='place_order'),
       path('handle_payment/<int:pk>/',handlepayment,name='handle_payment'),
       path('my_order/',myorder,name='my_order'),
       
       path('order_to_pdf/<int:pk>/', order_to_pdf,name = 'order_to_pdf'),
       path('chage_order_status/', chage_order_status,name = 'chage_order_status'),
              
       path('ajax_calls/search/', autocompleteModel,name = 'autocompleteModel'),
       path('search/', search,name = 'search'),
       path('my_profile/<int:pk>/', myProfile,name = 'my_profile'),
       path('change_username/<int:pk>/', Changeusername.as_view(),name = 'change_username'),
       path('edit_profile/<int:pk>/', ProfileUpdateview.as_view(),name = 'edit_profile'),
       path('like_product/<int:pk>/', like,name = 'like_product'),
       path('my_wishlist/<str:event>/', myWishlist,name = 'my_Wishlist'),
       
       path('contact/',Contactus.as_view(),name='contact_us'),
       path('bugreport/',BugreportView.as_view(),name='bug_report'),
       
]