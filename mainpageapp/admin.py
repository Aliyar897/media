from django.contrib import admin
from .models import ScrapedNewsData

@admin.register(ScrapedNewsData)
class ScrapedNewsDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'summary', 'summary_status', 'date_published', 'image', 'link', 'category', 'source')
