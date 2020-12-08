from django.db import models
from django import forms

# Create your models here.
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField


from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from datetime import date as tzdate


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    presentation = models.CharField(blank=False, max_length=150)
    role = models.CharField("Role (eg. Plant Expert)", blank=False, max_length=20, default="Plant Expert")

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('photo'),
        FieldPanel('presentation', classname="full"),
        FieldPanel('role'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True, default="")

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]

    def get_posts(self):
        return self.get_children().specific()

    def get_top_3(self):
        return self.get_children().specific()[:3]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.get_posts()
        context['categories'] = BlogCategory.objects.all()
        return context

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return BlogIndexPage.serve(self, request, *args, **kwargs)


class BlogPage(Page):
    date = models.DateField("Post date", default=tzdate.today)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    quote = models.CharField(max_length=250, default='', blank=True)

    author = models.ForeignKey('blog.Author', null=True, on_delete=models.SET_NULL)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('feed_image'),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('quote'),
        FieldPanel('author')
    ]

    parent_page_types = ['blog.BlogIndexPage']

    @property
    def parent_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['parent_page'] = self.parent_page
        context['all_categories'] = BlogCategory.objects.all()
        return context