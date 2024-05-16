import xml.etree.ElementTree as ET
from .models import Offer, Category, OfferColor


def parse_categories(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    cats = []
    for category_elem in root.findall(".//categories/category"):
        cat = Category()
        cat.name= category_elem.text
    
        cat.id  = int(category_elem.attrib["id"])
        cat.save()
        cats.append(cat)
    return str(cats.count())


def parse_offers(limit=10000, xml_file_path="base.xml", categories = None, ):


    if not categories: categories = parse_categories(xml_file_path)
    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    offers = []

    for offer_elem in root.findall(".//offer"):
        if limit > 0: limit -= 1
        else: break

        offer : Offer = Offer()
        offer.offer_id = int(offer_elem.attrib["id"])
        # offer.save()
        try:
            offer.category = Category.objects.get(id=int(offer_elem.find("categoryId").text))
        except:
            continue
            
        offer.parseModel(name=offer_elem.find("name_ua").text)
     
        offer.parseType(name=offer_elem.find("name_ua").text)

        try:
            offer.desc = offer_elem.find("description").text.strip()
        except:...
        try:
            offer.desc_ua = offer_elem.find("description_ua").text.strip()
        except:...
        try:
            offer.price = int(offer_elem.find("price").text)
        except:...
        try:
            offer.stock = int(offer_elem.find("stock_quantity").text) if int(offer_elem.find("stock_quantity").text) > 10  else 10
        except:...

        for param in offer_elem.findall(".//param"):
            if param.get("name") == "Цвет":
                # print(param.text)
                offer.color = OfferColor.objects.get(color_ua=param.text)

            elif param.get("name") == "Размер":
                offer.size = param.text
            elif param.get("name") == "Артикул":
                offer.article = param.text
            # offer.parameters.add(Parametr.objects.get(name=param.get("name")), value=param.text)
        
        if True:    
            offer.images = ""
            images = []
            for picture in offer_elem.findall("picture"):
                if picture.text: images.append(picture.text)
            if images: offer.images = offer.sortImages(images, article=offer.article)
        

        offer.save()
    offers.append(offer)

    return str(offers.count())