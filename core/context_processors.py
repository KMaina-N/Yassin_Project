# a context processor for displaying all the categories
# in the navbar
from .models import ProductCategory
def categories(request):
    return {
        'categories': ProductCategory.objects.all()
    }