from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.BuyerProductList.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('create_product/', views.ProductCreate.as_view(), name='create_product'),
    path('list_product', views.SellerProductList.as_view(), name='list_product'),
    path('detail_product/<int:pk>', views.ProductDetail.as_view(), name='detail_product'),
    path('delete_product/<int:pk>', views.ProductDelete.as_view(), name='delete_product'),
    path('update_product/<int:pk>', views.ProductUpdate.as_view(), name='update_product'),
    path('buyer_product_list', views.BuyerProductList.as_view(), name='buyer_list_product'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>', views.remove_from_cart, name='remove_from_cart'),
    path('remove_all_from_cart', views.remove_all_from_cart, name='remove_all_from_cart'),
    path('shopping_cart', views.shopping_cart, name='shopping_cart'),
    path('cep_locater', views.adress_completer, name='cep_locater'),
    path('credit_card', views.credit_card, name='credit_card'),
    path('final_screen', views.final_screen, name='final_screen')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
