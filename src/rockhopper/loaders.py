# rockhopper/loaders.py
import datetime
import hashlib
import toml
from types import SimpleNamespace

from django.conf import settings
from django.template.loader import render_to_string

from rockhopper import formats
from rockhopper.errors import LoadError
from rockhopper.models import Page, Tag, Category

# ===========================================================================
# Public Interface
# ===========================================================================

def load_groups():
    """Loads tags and categories from settings.ROCKHOPPER into the database"""
    for name in settings.ROCKHOPPER["CATEGORIES"]:
        Category.update_or_create(name=name)

    for name in settings.ROCKHOPPER["TAGS"]:
        Tag.update_or_create(name=name)


def load_file(path):
    # Check if the file is already in the CMS
    with open(path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")

    try:
        page = Page.objects.get(filename=str(path))
        if page.filehash == digest:
            # File hasn't changed
            return
    except Page.DoesNotExist:
        # Create a Page object without adding it to the database
        page = Page(filename=str(path), filehash=digest)

    suffix = path.suffix.lower()
    if suffix == 'toml':
        rh_type, context = _load_toml(path, page)
    else:
        raise LoadError(f"File suffix {suffix} is unknown")

    # Render content
    template_name = settings.ROCKHOPPER["TEMPLATES"][rh_type]
    content = render_to_string(template_name, context)
    page.content = content
    page.is_private = context['is_private']

    if 'slug' in context:
        page.slug = context['slug']
    else:
        page.slug = slugify(path.stem)

    if 'pubdate' in context:
        page.pubdate = datetime.strptime(context["pubdate"], "%y/%m/%d")
    else:
        page.pubdate = None


# ===========================================================================
# File Specific Loaders
# ===========================================================================

def _load_toml(path, page):
    text = path.read()
    toml_data = toml.loads(text)

    hopper = Hopper()
    if "rockhopper" not in toml_data:
        raise LoadError("No rockhopper meta data in toml content")

    if "type" not in toml_data["rockhopper"]:
        raise LoadError("No rockhopper type data in metadata")
    hopper.type = toml_data["rockhopper"]["type"]


    toml_data = SimpleNamespace(**toml_data)
    if hopper.type == "recipe":
        return formats.recipe(hopper)

    raise LoadError(f"TOML file with unknown hopper type {hopper.type}")
