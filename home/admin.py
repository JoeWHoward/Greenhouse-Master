from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from .models import Product

class ProductAdmin(ThumbnailMixin, ModelAdmin):
    model = Product
    menu_label = "Products"
    menu_icon = "form"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('__str__', 'admin_thumb', 'price', 'inventory')
    thumb_image_fieldname = 'image'


modeladmin_register(ProductAdmin)