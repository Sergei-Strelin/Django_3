from django.contrib import admin

# Register your models here.
from shop_app.models import Client, Goods, Order
from django.utils.html import format_html
#
# admin.site.register(Client)
# admin.site.register(Goods)
# admin.site.register(Order)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "email",
        ("phone", "address"),
        "create_at",
    )
    list_display = ("pk", "name", "email", "phone", "address", "create_at")
    list_display_links = ("pk", "name")
    list_editable = ("phone",)
    readonly_fields = ("create_at",)
    ordering = ("-pk", "name", "email", "phone", "address", "create_at")
    list_per_page = 10


@admin.register(Goods)
class GoodAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "description",
        ("price", "amount"),
        "create_at",
        ("image", "image_preview"),
    )
    list_display = ("pk", "name", "price", "amount", "create_at", "image_preview")
    list_display_links = ("pk", "name")
    list_editable = ("price", "amount")
    ordering = ("-pk", "name", "price", "amount", "create_at")
    readonly_fields = ("create_at", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No image"

    image_preview.short_description = "Image Preview"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = (
        "client",
        ("goods", "price"),
        "create_at",
        "date_edit_create_at",
        "goods_id",
    )
    list_display = ("pk", "client", "price", "create_at", "date_edit_create_at", "goods_id")
    list_display_links = ("create_at", "client")
    list_editable = ("price",)
    readonly_fields = ("create_at", "date_edit_create_at")
    ordering = ("-pk", "client", "price", "create_at", "date_edit_create_at", "goods")
    filter = ("price", "create_at", "client")