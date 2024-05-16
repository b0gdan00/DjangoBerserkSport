from datetime import datetime
import os
import xml.etree.ElementTree as ET

from django.conf import settings
from .models import Offer, Category, SIZE_FOR_KIDS, KIDS_CAT


class XMLBuilder:

    url             = "https://berserk-sport.com/"
    # savePath        : str = "new.xml"
    # savePathRZ      : str = "RZ.xml"
    # savePathHubber  : str = "hubber.xml"
    currencies      = [{"id": "UAH", "rate": 1}]
    vendor          = "BERSERK SPORT"

    def __init__(self, savePath = None) -> None:
        if savePath: self.savePath = savePath
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def generate(self, offers : list[Offer], categories : list[Category]):
        if not offers: return False
        root = ET.Element("yml_catalog", attrib={"date": self.date})
        shop = ET.SubElement(root, "shop")
        ET.SubElement(shop, "company").text = self.vendor
        ET.SubElement(shop, "url").text = self.url
        currencies_element = ET.SubElement(shop, "currencies")
        for currency in self.currencies: ET.SubElement(currencies_element, "currency", attrib={"id": currency["id"], "rate": str(currency["rate"])})
        
        categories_element = ET.SubElement(shop, "categories")
        for category in categories:
            ET.SubElement(categories_element, "category", attrib={"id": str(category.id)}).text = category.name
        
        
        offers_element = ET.SubElement(shop, "offers")
        for offer in offers:
            kids = False
            if str(offer.category.id) in KIDS_CAT.split(): kids = True

            offer_element = ET.SubElement(offers_element, "offer", attrib={"id": str(offer.offer_id), "available": str(offer.enable).lower()})


            ET.SubElement(offer_element, "vendor").text     = self.vendor
            ET.SubElement(offer_element, "article").text    = offer.article
            ET.SubElement(offer_element, "name").text       = offer.name_ru
            ET.SubElement(offer_element, "name_ua").text    = offer.name_ua
            ET.SubElement(offer_element, "price").text      = str(offer.price)
            ET.SubElement(offer_element, "currencyId").text = "UAH"
            ET.SubElement(offer_element, "categoryId").text = str(offer.category.id)
            ET.SubElement(offer_element, "stock_quantity").text = str(offer.stock)
            ET.SubElement(offer_element, "description").text    = offer.desc
            ET.SubElement(offer_element, "description_ua").text = offer.desc_ua


            for picture in offer.images.split("\n"):
                if picture.strip(): ET.SubElement(offer_element, "picture").text    = picture.strip()

            ET.SubElement(offer_element, "param", attrib={"name": "Цвет"}).text     = offer.color.color_ru
            ET.SubElement(offer_element, "param", attrib={"name": "Колір"}).text    = offer.color.color_ua
            ET.SubElement(offer_element, "param", attrib={"name": "Розмір"}).text   = offer.size
            ET.SubElement(offer_element, "param", attrib={"name": "Размер"}).text   = offer.size
            if kids:
                ET.SubElement(offer_element, "param", attrib={"name": "Зріст"}).text   = SIZE_FOR_KIDS.get(offer.size.upper(), "140 - 153 см") 
                ET.SubElement(offer_element, "param", attrib={"name": "Рост"}).text   = SIZE_FOR_KIDS.get(offer.size.upper(), "140 - 153 см")


            
        media_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        with open(os.path.join(media_dir, "new.xml"), "wb") as f: f.write(ET.tostring(root, encoding="utf-8"))
        return True
                


                
    