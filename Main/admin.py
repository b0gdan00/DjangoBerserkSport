from django.contrib import admin
from .models import Offer, OfferType, Category, OfferColor, UploadFiles
from .XML import parse_offers, parse_categories
from .XML_builder import XMLBuilder

# admin.site.register(Offer)
# admin.site.register(OfferType)
# admin.site.register(Category)
# admin.site.register(OfferColor)
# # admin.site.register(Image)
# admin.site.register(Parametr)

def build(modeladmin, request, queryset):
    
    for offers in queryset:
        print(offers)
    builder = XMLBuilder()
    print("res: "+str(builder.generate(queryset, Category.objects.all()))) 
    
    modeladmin.message_user(request, f"Створено файл з {len(queryset)} товарами")


def loadOffers(modeladmin, request, queryset):
        for upload_file in queryset:
             modeladmin.message_user(request, "Оновлено: "+upload_file.load(parse_offers)+ " товарів")

def loadCategories(modeladmin, request, queryset):
        for upload_file in queryset:
            
            modeladmin.message_user(request,"Оновлено: "+upload_file.load(parse_categories)+ " категорій")

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'model', 'category', 'offer_type')
    list_filter = ('category', 'offer_type', "color", "size")
    build.short_description = "Створити вигрузку Rozetka"
    actions = [build]

@admin.register(UploadFiles)
class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

    actions = [loadOffers, loadCategories]


admin.site.register(OfferType)
admin.site.register(Category)
admin.site.register(OfferColor)
# admin.site.register(Parametr)


