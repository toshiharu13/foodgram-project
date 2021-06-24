import importlib
from prod_h.models import Amount, ListOfIngridients
from django.http import HttpResponse
from decimal import Decimal
from reportlab.pdfbase import pdfmetrics
from django.shortcuts import get_object_or_404
from reportlab.pdfbase.ttfonts import TTFont
module = importlib.import_module('.settings', 'foodgram-project')
from reportlab.pdfgen import canvas

def get_tags(request):
    # Get tags list
    tags_list = []
    for key in request.POST.keys():
        if key in module.TAGS:
            tags_list.append(key)
    return tags_list

def get_ingredients(request, recipe):
    # Add Ingredients to New Recipe.
    ist_of_ingredients = []
    name_of_ingredient = None
    for key, value in request.POST.items():
        if 'nameIngredient' in key:
            name_of_ingredient = value
        if 'valueIngredient' in key:
            #amount = Decimal(value.replace(',', '.'))
            if value == None or value == 0 or value == '':
                value = 1
            amount = value
            ingredient = get_object_or_404(ListOfIngridients, name=name_of_ingredient)
            Amount.objects.get_or_create(
                    ingredient=ingredient,
                    recipe=recipe,
                    counts=amount)[0]
            ist_of_ingredients.append(ingredient)
    return ist_of_ingredients

def tags_filter(request):
    # Get actual tags
    tags_list = request.GET.getlist('tag', module.TAGS)
    return tags_list

def download_pdf(data):
    """Download shopping list in pdf format"""
    # Create the HttpResponse object with the appropriate PDF headers.
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="List product.pdf"'
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    p.setFont('DejaVuSans', 15)
    # Draw things on the PDF. Here's where the PDF generation happens.
    p.drawString(100, 800, "Список продуктов:")
    x, y = 10, 780
    for item in data:
        p.drawString(x, y, item.get('item__ingredients__name')
                     + ' ' + '(' + item.get('item__ingredients__units_of_measurement') + ')'
                     + ' - ' + str(item.get('amount')))
        y -= 15
        p.showPage()
        p.save()
        return response