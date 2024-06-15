from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Perfume
# Create your views here.

def index(request):
    perfumes = Perfume.objects.all()

    # search code
    item_name = request.GET.get('item_name', '').strip()

    if item_name != '' and item_name is not None:
        perfumes = perfumes.filter(name__icontains=item_name) | perfumes.filter(brand__icontains=item_name)

    # pagination code
    paginator = Paginator(perfumes, 24)
    page = request.GET.get('page')

    try:
        perfumes = paginator.page(page)
    except PageNotAnInteger:
        perfumes = paginator.page(1)


    return render(request, 'perfumeshop/index.html', {'perfumes': perfumes})

