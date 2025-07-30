from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from .models import Place, Image
from django.utils.html import format_html


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ['image', 'image_preview', 'position']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" />',
                obj.image.url
            )

    image_preview.short_description = "Превью"

@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    raw_id_fields = ['place']
