from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.db import models

from artd_product.models import (
    Tax,
    RootCategory,
    Category,
    Brand,
    Product,
    ProductImage,
    GroupedProduct,
)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "percentage",
        "status",
    )
    list_filter = (
        "name",
        "percentage",
        "status",
    )
    search_fields = (
        "name",
        "percentage",
        "status",
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    # Create BrandAdmin


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    list_filter = (
        "name",
        "status",
    )
    search_fields = (
        "name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )


@admin.register(RootCategory)
class RootCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    list_filter = (
        "name",
        "status",
    )
    search_fields = (
        "name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    list_filter = (
        "name",
        "status",
        "parent",
    )
    search_fields = (
        "name",
        "parent__name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )
    list_filter = (
        "name",
        "brand",
        "status",
    )
    search_fields = (
        "name",
        "brand__name",
        "status",
        "url_key",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "image",
        "alt",
        "status",
    )
    list_filter = (
        "product",
        "status",
    )
    search_fields = (
        "product__name",
        "status",
    )


@admin.register(GroupedProduct)
class GroupedProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "sku",
        "status",
    )
