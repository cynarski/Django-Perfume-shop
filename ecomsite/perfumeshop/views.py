from django.shortcuts import render
from .models import Perfume
# Create your views here.

def index(request):
    perfumes = Perfume.objects.all()
    return render(request, 'perfumeshop/index.html', {'perfumes': perfumes})

