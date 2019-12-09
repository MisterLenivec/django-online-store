from .models import Category


def categories_base(request):
    categories = Category.objects.all()
    return {'categories': categories}
