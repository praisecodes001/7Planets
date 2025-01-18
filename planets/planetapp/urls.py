from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import PostListView, PostDetailView
from django.conf import settings






urlpatterns = [
    path('home', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('conditions/', views.conditions, name="conditions"),
    path('login/', views.loginPage, name="login"),
    path('clear-orders/', views.clear_orders, name='clear_orders'),
    path('order_success/', views.order_success, name="order_success"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/', views.PostListView.as_view(), name="product"),
    path('cart/remove/<int:post_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('dashboard/order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path("logout/", views.logoutUser, name="logout"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

