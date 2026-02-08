from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from django.core.paginator import Paginator


@login_required
def home_view(request):
    return render(request, 'products/home.html')

@login_required

def sell_view(request):

    categories = Category.objects.all()

    if request.method=="POST":
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if not title or not description or not price:
            messages.error(request, "All required fields must be filled.")
            return render(request, 'products/sell.html', {'categories': categories})
        

        category = None
        if category_id !='':
            category = Category.objects.get(id = category_id)

        Product.objects.create(
            seller=request.user,
            category=category,
            title=title,
            description=description,
            price=price,
            condition=condition,
            image=image
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