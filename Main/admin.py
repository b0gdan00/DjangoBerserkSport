from django.contrib import admin
from .models import Offer, OfferType, Category, OfferColor, UploadFiles
from .XML import parse_offers, parse_categories
from django.utils.html import format_html

# admin.site.register(Offer)
# admin.site.register(OfferType)
# admin.site.register(Category)
# admin.site.register(OfferColor)
# # admin.site.register(Image)
# admin.site.register(Parametr)

def loadOffers(modeladmin, request, queryset):
        for upload_file in queryset:
            upload_file.load(parse_offers)

def loadCategories(modeladmin, request, queryset):
        for upload_file in queryset:
            upload_file.load(parse_categories)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'model', 'category', 'offer_type')
    list_filter = ('category', 'offer_type', "color", "size")

@admin.register(UploadFiles)
class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

    actions = [loadOffers, loadCategories]


admin.site.register(OfferType)
admin.site.register(Category)
admin.site.register(OfferColor)
# admin.site.register(Parametr)


