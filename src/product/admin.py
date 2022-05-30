from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from feature.models import GroupsFeature
from .models import (
    Brand,
    ProducingCountry,
    Category, 
    SubCategory, 
    ProductType,
    # Product,
    Store
)


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    save_as = True


@admin.register(Store)
class StoreAdmin(ImportExportModelAdmin):
    list_display = ['name', 'url_link']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    save_as = True


@admin.register(ProducingCountry)
class ProducingCountryAdmin(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    save_as = True


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'icon_tag', 'id']
    search_fields = ['name']
    save_as = True


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']
    save_as = True


class GroupsFeatureInline(admin.TabularInline):

    model = GroupsFeature
    extra = 0


@admin.register(ProductType)
class ProductTypeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'subcategory']
    search_fields = ['name']
    inlines = [GroupsFeatureInline]
    prepopulated_fields = {'slug': ('name',)}
    save_as = True


# @admin.register(Product)
# class ProductAdmin(ImportExportModelAdmin):
#     list_display = ['name', 'product_type', 'subcategory', 'product_id', 'sync_id', 'vendor_code']
#     search_fields = ['name']
#     prepopulated_fields = {'slug': ('name',)}
#     save_as = True
