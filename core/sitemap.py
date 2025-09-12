from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['landing', 'about', 'create_review', 'service_list']

    def location(self, item):
        return reverse(item)

    # Переопределяем URL, чтобы использовать текущий домен
    def get_urls(self, site=None, **kwargs):
        site = type('obj', (object,), {
            'domain': '127.0.0.1:8000',  # Укажите ваш домен
            'name': 'Mi Mary'
        })
        return super().get_urls(site=site, **kwargs)

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Category.objects.all()
    
    def location(self, obj):
        return reverse('category_services', args=[obj.id])

    # Аналогично переопределяем домен
    def get_urls(self, site=None, **kwargs):
        site = type('obj', (object,), {
            'domain': '127.0.0.1:8000',
            'name': 'Mi Mary'
        })
        return super().get_urls(site=site, **kwargs)