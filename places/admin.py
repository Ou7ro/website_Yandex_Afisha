from django.contrib import admin
from .models import Place, Image
from django.utils.safestring import mark_safe

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview', 'position']
    
    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="200" />')

class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    

admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
