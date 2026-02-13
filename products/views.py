from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, ProductImage
from django.core.paginator import Paginator


@login_required
def home_view(request):
    return render(request, 'products/home.html')

@login_required

def sell_view(request):

    categories = Category.objects.all()

    profile = getattr(request.user,'profile', None)

    if not profile or not(profile.department and profile.batch and profile.phone):
        messages.error(request,"Please complete your profile before listing a product.")
        return redirect("profile")

    if request.method=="POST":
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        category_id = request.POST.get('category')
        images = request.FILES.getlist('images')

        if not title or not description or not price:
            messages.error(request, "All required fields must be filled.")
            return render(request, 'products/sell.html', {'categories': categories})
        

        category = None
        if category_id !='':
            category = Category.objects.get(id = category_id)

        product = Product.objects.create(
            seller=request.user,
            category=category,
            title=title,
            description=description,
            price=price,
            condition=condition
        )

        # Save multiple images
        for idx, image in enumerate(images):
            ProductImage.objects.create(
                product=product,
                image=image,
                order=idx
            )

        messages.success(request, "Product listed successfully!")
        return redirect('sell')

    return render(request, 'products/sell.html', {'categories': categories})


@login_required
def buy_view(request):
    products = Product.objects.filter(is_available = True).order_by('-created_at')
    categories = Category.objects.all()

    q = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    condition = request.GET.get('condition', '').strip()


    if q:
        products = products.filter(title__icontains = q)
    if category_slug:
        products = products.filter(category__slug = category_slug)
    if condition in ['NEW', 'USED']:
        products = products.filter(condition=condition)

    paginator = Paginator(products,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,

        # keep selected values in template
        'q': q,
        'category_slug': category_slug,
        'condition': condition,
    }


    return render(request, 'products/buy.html', context)

def product_detail_view(request,pk):
    product = get_object_or_404(Product,pk=pk)
    context = {
        "product": product,
    }
    return render(request,'products/product_detail.html',context)


@login_required
def my_products_view(request):
    products = Product.objects.filter(seller = request.user).order_by('-created_at')
    context = {
        "products": products,
    }
    return render(request,'products/my_product.html',context)

@login_required
def product_edit_view(request,pk):
    product = get_object_or_404(Product,pk=pk)
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get("title", '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if not title or not description or not price:
            messages.error(request, "All required fields must be filled.")
            return render(request, 'products/product_edit.html', {
                'product': product,
                'categories': categories,
            })
        
        category = None
        if category_id:
            category = Category.objects.filter(id=category_id).first()

        # update fields
        product.title = title
        product.description = description
        product.price = price
        product.condition = condition
        product.category = category

        # update image only if new file selected
        if image:
            product.image = image

        product.save()

        messages.success(request, "Product updated successfully!")
        return redirect('product_detail', pk=product.pk)

    return render(request, 'products/product_edit.html', {
        'product': product,
        'categories': categories,
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        messages.error(request, "You are not allowed to delete this product.")
        return redirect('buy')

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('my_products_view')

    return render(request, 'products/product_delete.html', {'product': product})

@login_required
def toggle_product_status(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.seller != request.user:
        messages.error(request, "You are not allowed to modify this product.")
        return redirect('buy')
    
    product.is_available = not product.is_available
    product.save()
    
    status = "available" if product.is_available else "sold"
    messages.success(request, f"Product marked as {status}!")
    return redirect('my_products_view')