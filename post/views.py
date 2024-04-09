from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from blog import settings
from .forms import ProductCreateForm, ProductCreateForm2, CommentCreateForm, CategoryCreateForm
from .models import Product, HashTag, Category, Comment


class MainView(View):
    def get(self, request):
        return render(request, 'layouts/index.html')


class CategoryProductsView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = category.products.all()
        context = {
            'category': category,
            'products': products,
        }
        return render(request, 'categories/category_products.html', context)


class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()
        context = {
            "categories": categories,
        }
        return render(request, 'categories/categories.html', context=context)


class ProductsView(View):
    @login_required
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        selected_category = request.GET.get('category')
        search = request.GET.get('search')
        order = request.GET.get('order')
        if selected_category:
            category = get_object_or_404(Category, title=selected_category)
            products = products.filter(category=category)
        elif search:
            products = products.filter(
                Q(title__icontains=search)
            )
        elif order == 'title':
            products = products.order_by('title')
        elif order == '-title':
            products = products.order_by('-title')
        elif order == 'created_at':
            products = products.order_by('created_at')
        elif order == '-created_at':
            products = products.order_by('-created_at')
        else:
            products = products.exclude(user=request.user)

        max_page = products.count() / settings.PAGE_SIZE
        max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)

        page = int(request.GET.get('page', 1))

        start = (page - 1) * settings.PAGE_SIZE
        end = page * settings.PAGE_SIZE

        products = products[start:end]

        context = {
            "products": products,
            "selected_category": selected_category,
            "categories": categories,
            "pages": range(1, max_page + 1)
        }
        return render(request, 'products/products.html', context=context)


class ProductDetailView(View):
    def get(self, request, product_id=None):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return render(request, 'errors/404.html')
        context = {
            "product": product,
            'form': CommentCreateForm()
        }
        return render(request, 'products/product_detail.html', context)

    def post(self, request, product_id=None):
        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            Comment.objects.create(product_id=product_id, **form.cleaned_data)
            return redirect(f'/product/{product_id}/')
        context = {
            'form': form,
        }
        return render(request, 'products/product_detail.html', context)


class ProductUpdateView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        context = {
            "form": ProductCreateForm(instance=product)
        }
        return render(request, 'products/product_update.html', context)

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = ProductCreateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(f'/products/{product.id}/')
        return render(request, 'products/product_update.html', {"form": form})


class ProductCreateView(View):
    def get(self, request):
        context = {
            "form": ProductCreateForm2()
        }
        return render(request, 'products/products.create.html', context)

    def post(self, request):
        form = ProductCreateForm2(request.POST, request.FILES)
        if form.is_valid():
            Product.objects.create(**form.cleaned_data)
            return redirect("/products/")
        context = {
            "form": form
        }
        return render(request, 'products/products.create.html', context)


class CategoryCreateView(View):
    def get(self, request):
        context = {
            "form": CategoryCreateForm(),
        }
        return render(request, 'categories/categories_create.html', context=context)

    def post(self, request):
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            Category.objects.create(**form.cleaned_data)
            return redirect('/categories/')
        context = {
            "form": form
        }
        return render(request, 'categories/categories_create.html', context=context)


class HashtagsView(View):
    def get(self, request):
        hashtags = HashTag.objects.all()
        context = {
            "hashtags": hashtags,
        }
        return render(request, 'hashtags/hashtags.html', context=context)
