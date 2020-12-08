from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from blog.models import BlogPage, Author
from django.core.validators import MaxValueValidator, MinValueValidator
import re

class HomePage(Page):
    """Home page model."""

    def blogs(self):
        blogs = BlogPage.objects.all()
        blogs = blogs.order_by('-date')[:3]
        return blogs

    templates = "home/home_page.html"
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold","italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
 #   logo_image = models.ForeignKey(
 #       "wagtailimages.Image",
 #       null=True,
 #       blank=False,
 #       on_delete=models.SET_NULL,
 #       related_name="+",
 #   )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    max_count = 1
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
#        ImageChooserPanel("logo_image"),
        PageChooserPanel("banner_cta"),
    ]
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    def get_context(self, request):
        context = super().get_context(request)
        context['authors'] = Author.objects.all()

        return context


class StorePage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        context['products'] = Product.objects.child_of(self).live()

        return context

class Product(Page):
    sku = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    star_rating = models.IntegerField("Star Rating (0-5)", max_length=1, default=2, validators=[MaxValueValidator(5), MinValueValidator(0)])
    inventory = models.IntegerField("Inventory In Stock", blank=True, help_text="Put a really high number for 'infinite' stock", default=0)
    
    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        clean_fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split('|')
                f.clean_options_array = [re.sub("[\(\[].*?[\)\]]", "", i) for i in f.options_array]
                fields.append(f)
            else:
                fields.append(f)
        
        context['custom_fields'] = fields

        return context

    content_panels = Page.content_panels + [
        FieldPanel('sku'),
        FieldPanel('price'),
        ImageChooserPanel('image'),
        FieldPanel('short_description'),
        InlinePanel('custom_fields', label='Custom fields'),
    ]

class ProductCustomField(Orderable):
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]

@register_setting
class SnipcartSettings(BaseSetting):
    api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )