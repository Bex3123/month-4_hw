from django.urls import path
from .views import (
    MainView, CategoryProductsView, CategoriesView, ProductsView,
    ProductDetailView, ProductUpdateView, ProductCreateView,
    CategoryCreateView, HashtagsView
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
    path('products/', ProductsView.as_view(), name='products'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('hashtags/', HashtagsView.as_view(), name='hashtags'),
]
