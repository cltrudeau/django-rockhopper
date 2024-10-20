# rockhopper.formats.py
import re

from django.conf import settings
import mistune

from rockhopper.errors import LoadError

# ===========================================================================
# Hopper Container
# ===========================================================================

class Hopper:
    def __init__(self):

        ??? put RH context stuff here?

        ??? Move this to loaders.py?


# ===========================================================================
# Recipe
# ===========================================================================

MEASURES = ['tsp', 'Tbsp', 'cup', 'cups', 'can', 'ml', 'L', 'g', 'oz', '',
    'lbs', 'pinch', 'clove', 'cloves', 'slice', 'slices', 'dash', 'packet',
    'packets', 'container', 'containers', 'shot', 'shots']

FRACTION_MAP = {
    '1/4':'¼',
    '3/4':'¾',
    '1/2':'½',
    '1/3':'⅓',
    '2/3':'⅔',
    '1/8':'⅛',
    '3/8':'⅜',
    '5/8':'⅝',
    '7/8':'⅞',
}

def recipe(content, page):
    r = content.recipe

    # Pure text values
    data = {
        'is_private': getattr(content.rockhopper.private, False),
        'title': getattr(r, 'title', ''),
        'serves': getattr(r, 'serves', ''),
        'cooktime': getattr(r, 'cooktime', ''),
        'tags': [],
        'ingredients': [],
        'ingredient_parts': [],
    }

    name = getattr(r, 'category', '')
    if cat:
        try:
            data['category'] = Category.get(name=name)
        except Category.DoesNotExist:
            raise LoadError(f"No such category: {name}")

    tag_names = getattr(r, 'tags', ''):
    if tag_names:
        for name in tag_names:
            try:
                data['tags'].append = Tag.get(name=name)
            except Tag.DoesNotExist:
                raise LoadError(f"No such tag: {name}")

    # Markdown based attributes
    for attr in ["description", "steps", "notes"]:
        text = getattr(r, attr, '')
        if not text:
            continue

        # Replace any fraction strings with their character equivalent
        for key, value in FRACTION_MAP.items():
            text = re.sub(key, value, text)

        data[attr] = mistune.html(text)

    # Validate ingredients
    ingredients = getattr(r, 'ingredients', ''):
    if ingredients:
        for i in ingredients:
            if i[1] not in MEASURES:
                warn(f"Unknown measure found: {i[1]}")

        data["ingredients"] = ingredients

    ingredient_parts = getattr(r, 'ingredient_parts', ''):
    if ingredient_parts:
        for i in ingredient_parts.values():
            if i[1] not in MEASURES:
                warn(f"Unknown measure found: {i[1]}")

        data["ingredient_parts"] = ingredient_parts

    return data
