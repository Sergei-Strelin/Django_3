# from django.conf.urls.static import static
# from django.conf import settings
from django.urls import path
from shop_app import views
from .views import all_clients, orders_by_client, order_full, edit_good, good_full, upload_images, upload_images1

app_name = 'shop_app'

urlpatterns = [
    path("", all_clients, name="all_clients"),
    path('clients/', views.get_clients, name='clients'),
    path('goods/', views.get_goods, name='goods'),
    path('orders/', views.get_orders, name='orders'),
    path('client_orders/<int:client_id>', views.get_orders_by_client_id, name='client_orders'),
    path('delete_client/<int:client_id>', views.delete_client, name='delete_client'),
    path('delete_goods/<int:goods_id>', views.delete_goods, name='delete_goods'),
    path('delete_order/<int:order_id>', views.delete_order, name='delete_order'),
    path('edit_client_name/<int:client_id>/<str:name>', views.edit_client_name, name='edit_client_name'),
    path('edit_goods_price/<int:goods_id>/<int:price>', views.edit_goods_price, name='edit_goods_price'),
    path('edit_order_goods_id/<int:order_id>/<int:goods_id>', views.edit_order_goods_id, name='edit_order_goods_id'),
    path('client_goods/<int:client_id>', views.get_client_goods, name='get_client_goods'),
    path('test/', views.test, name='test'),
    path('main/', views.main, name='main'),
    path('client_goods/', views.client_goods, name='client_goods'),
    path('contacts/', views.contacts, name='contacts'),
    path('get_catalog/', views.get_catalog, name='get_catalog'),

    path("edit/<int:good_pk>", edit_good, name="edit_good"),
    path("edit/", views.get_edit_good, name="get_edit_good"),
    path("client/<int:client_pk>", orders_by_client, name="orders_by_client"),
    path("order/<int:order_pk>", order_full, name="order_full"),
    path("good/<int:good_pk>", good_full, name="good_full"),
    path('upload_images/', upload_images, name="images"),
    path('upload_images1/', upload_images1, name="images"),

]

# включаем возможность обработки картинок
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)