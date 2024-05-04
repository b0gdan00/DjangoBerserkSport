import xml.etree.ElementTree as ET
from .models import Image, Offer, Category, OfferColor, Parametr, SIZE_CHOICES


def parse_categories(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    for category_elem in root.findall(".//categories/category"):
        cat = Category()
        cat.name= category_elem.text
    
        cat.id  = int(category_elem.attrib["id"])
        cat.save()


def parse_offers(limit=10000, xml_file_path="base.xml", categories = None, ):


    # if not categories: categories = parse_categories()
    
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
            print("Параметр відсутній", f"( {str(offer.offer_id)} )\t category")
            continue
            
        offer.parseModel(name=offer_elem.find("name_ua").text)
     
        offer.parseType(name=offer_elem.find("name_ua").text)

        try:
            offer.desc = offer_elem.find("description").text.strip()
        except:
            print("Параметр відсутній", f"( {str(offer.offer_id)} )\t desc")
        try:
            offer.desc_ua = offer_elem.find("description_ua").text.strip()
        except:
            print("Параметр відсутній", f"( {str(offer.offer_id)} )\t desc_ua")
        try:
            offer.price = int(offer_elem.find("price").text)
        except:
            print("Параметр відсутній", f"( {str(offer.offer_id)} )\t price")
        try:
            offer.stock = int(offer_elem.find("stock_quantity").text) if int(offer_elem.find("stock_quantity").text) > 10  else 10
        except:
            print("Параметр відсутній", f"( {str(offer.offer_id)} )\t stock")
        if True:    
            [Image.objects.get_or_create(url=pic.text)[0] for pic in offer_elem.findall("picture")]
            
            for i in offer_elem.findall("picture"):
                offer.images.add(Image.objects.get(url=i.text))
        
        for param in offer_elem.findall(".//param"):
            if param.get("name") == "Цвет":
                try:offer.color = OfferColor.objects.get(color_ua=param.text)
                except: offer.color = OfferColor.objects.all().first()
            elif param.get("name") == "Размер":
                offer.size = param.text
            elif param.get("name") == "Артикул":
                offer.article = param.text
            # offer.parameters.add(Parametr.objects.get(name=param.get("name")), value=param.text)


        offer.save()
    offers.append(offer)

    # return offers