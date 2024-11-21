from django.shortcuts import render
from shop.models import Product

# Create your views here.
from django.db.models import Q
def searchproducts(request):
    p = None
    query = ""
    if (request.method == "POST"):  # after form submission
        query = request.POST['q']
        print(query)
        if query:
            p = Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))  # django lookups

    return render(request, 'search.html', context={'pro': p, 'query': query})
