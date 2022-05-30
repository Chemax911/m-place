# from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
#
# from feature.models import FeatureKey, FeatureValue, GroupsFeature
#
#
# class FeatureValueInline(admin.TabularInline):
#
#     model = FeatureValue
#     extra = 0
#
#
# class FeatureKeyInline(admin.TabularInline):
#
#     model = FeatureKey
#     extra = 0
#
#
# @admin.register(GroupsFeature)
# class GroupsFeatureAdmin(ImportExportModelAdmin):
#     list_display = ['name', 'product_type']
#     search_fields = ['name']
#     inlines = [FeatureKeyInline]
#     save_as = True
#
#
# @admin.register(FeatureKey)
# class FeatureKeyAdmin(ImportExportModelAdmin):
#     list_display = ['name', 'group', 'slug', 'kind']
#     search_fields = ['name']
#     inlines = [FeatureValueInline]
#     save_as = True
#
#
# @admin.register(FeatureValue)
# class FeatureValueAdmin(ImportExportModelAdmin):
#     list_display = ['value', 'features', 'product']
#     search_fields = ['value']
#     save_as = True
