from django.contrib import admin
from .models import Offer, OfferType, Category, OfferColor, Parametr


admin.site.register(Offer)
admin.site.register(OfferType)
admin.site.register(Category)
admin.site.register(OfferColor)
# admin.site.register(Image)
admin.site.register(Parametr)