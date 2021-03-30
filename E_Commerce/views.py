from django.shortcuts import render

from .models import (
    Product,
    Category,
    sub_category,
    Cart,
    HomeBanner,
    size,
    User,
    UserProfile,
    )


# Create your views here.

def index_view(request):
    request.session['category'] = "kurti, saree, suit"
    request.session.set_expiry(0)
    catprods = []
    cat_list = []
    home_banner = HomeBanner.objects.all()
    category = Category.objects.values_list()
    for i in category:
        getprod = Product.objects.filter(category=i[0])
        if len(getprod) > 0:
            catprods.append(getprod)
            cat_list.append(i[1])

    context = {
        'catprods': catprods,
        'cat_list': cat_list,
        'home_banner': home_banner,
    }
    response = render(request, 'ecommerce/index.html', context)
    # response.set_cookie('name', 'rimmy', expires=datetime.utcnow() + timedelta(days=2))  # 10 seconds
    return response
