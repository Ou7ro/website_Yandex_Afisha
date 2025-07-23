from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from .models import Place, Image
from django.utils.safestring import mark_safe


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ['image', 'image_preview', 'position']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="200" />')

    image_preview.short_description = "Превью"


class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
