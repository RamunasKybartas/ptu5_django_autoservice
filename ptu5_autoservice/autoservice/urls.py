from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list_view, name='cars'),
    path('car/<int:pk>/', views.car_detail_view, name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('my_orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('create_new_order/', views.UserNewOrderCreateView.as_view(), name='user_create_new_order'),
    path('update_order/<int:pk>/', views.UserOrderUpdateView.as_view(), name='user_update_order'),
    path('cancel_order/<int:pk>/', views.UserOrderDeleteView.as_view(), name='user_delete_order'),
]