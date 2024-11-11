from django.urls import path
from .views import (
    RegisterView, LoginView, CategoryListView, ProductListView,
    CartView, AddToCartView, PurchaseView, ProductListByCategoryView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/products/', ProductListByCategoryView.as_view(), name='product-list-by-category'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
]
