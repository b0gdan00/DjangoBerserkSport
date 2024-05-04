from enum import Enum, auto
import re
from django.db import models
from fuzzywuzzy import process

EXCLUDES    = [
    "black red pink dark gray grey white yellow blue green orange olive brown purple violet light multi",
    "в наявності розмір наличии размер спортивные спортивный флисовая BERSERK SPORT KID компрессионные компресійні для борьбы боротьби",
]


TYPES_UA    = ["футболка", "бриджі", "штани", "шорти", "лосіни", "костюм", "легінси", "напульсник", "худі", "рашгард", "нарукавник","трико", "світшот", "кофта", "майка", "топ", "індіма", "комбінезон", "реглан"]
TYPES       = ["футболка", "бриджи", "штаны", "шорты", "костюм", "легинсы", "напульсник", "лосини", "нарукавник", "худи", "рашгард", "трико", "свитшот", "кофта", "майка", "топ", "индима", "комбинезон", "реглан"]
SIZES       = "m l s xs 2xs 3xs 4xs 5xs xl 2xl 3xl 4xl 5xl xxl xxxl xxs xxxs xsy"
SIZE_FOR_KIDS = {
    "M"     : "160 - 165 см",
    "XS"    : "158 см",
    "2XS"   : "152 см",
    "XXS"   : "152 см",
    "3XS"   : "146 - 152 см",
    "XXXS"   : "146 - 152 см",
    "4XS"   : "134 - 140 см",
    "XXXXS"   : "134 - 140 см",
    "5XS"   : "134 см"    
}

SIZE_CHOICES = (
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("2XL", "2XL"),
    ("3XL", "3XL"),
    ("4XL", "4XL"),
    ("5XL", "5XL"),
    ("2XS", "2XS"),
    ("3XS", "3XS"),
    ("4XS", "4XS"),
    ("5XS", "5XS"),
)

PARAMETR_CHOICES = (
    ("Color", "Цвет"),
    ("Size", "Размер"),
    ("Article", "Артикл"),
    ("Material", "Матеріал"),
    ("Country of production", "Країна виробника"),
    ("Description", "Опис російською"),
    
    # ("Колір", "Color"),
    # ("Розмір", "Size"),
    # ("Артикл", "Article"),
    # ("Матеріал", "Material"),
    # ("Країна виробника", "Country of production"),
    # ("Призначення", "Description"),
    # ("Стиль", "Style"),
)

EXCLUDES    = [word.lower() for phrase in EXCLUDES for word in phrase.split()]
EXCLUDES    .extend(TYPES)
EXCLUDES    .extend(TYPES_UA)



class OfferType(models.Model):

    class Meta:
        verbose_name_plural = "Типи товарів"

    name_ua  = models.CharField(max_length=255)
    name_ru  = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name_ua

    
class OfferColor(models.Model):

    class Meta:
        verbose_name_plural = "Кольори"

    color_en    = models.CharField(max_length=255, verbose_name="Колір англійською")
    color_ua    = models.CharField(max_length=255, verbose_name="Колір українською")
    color_ru    = models.CharField(max_length=255, verbose_name="Колір російською")

    def __str__(self) -> str:
        return self.color_ua


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Категорії"
    
    id      = models.BigIntegerField(verbose_name="Айді", primary_key=True)
    name    = models.CharField(max_length=255, verbose_name="Назва")

    def __str__(self) -> str:
        return self.name

class Parametr(models.Model):

    class Meta:
        verbose_name_plural = "Параметри"

    parametr_id    = models.BigIntegerField(verbose_name="Параметр айді", primary_key=True)
    parametr_name  = models.CharField(verbose_name="Назва", choices=PARAMETR_CHOICES, max_length=1000, blank=False)
    parametr_value = models.CharField(verbose_name="Значення", max_length=1000, blank=False)

    def __str__(self) -> str:
        return self.parametr_name

class Image(models.Model):

    class Meta:
        verbose_name_plural = "Зображення"

    url     = models.URLField(verbose_name="URL", unique=True)

    def __str__(self) -> str:
        return self.url


class Offer(models.Model):

    class Meta:
        verbose_name_plural = "Товари"

    offer_id    = models.BigIntegerField(verbose_name="Офер айді", primary_key=True)
    offer_type  = models.ForeignKey(OfferType, verbose_name="Тип товару", on_delete=models.CASCADE, blank=True, null=True)
    model       = models.CharField(verbose_name="Модель", max_length=1000)
    size        = models.CharField(verbose_name="Розмір товару", max_length=255, choices=SIZE_CHOICES, blank=True)

    category    = models.ForeignKey(Category, verbose_name="Категорія", on_delete=models.CASCADE)
    color       = models.ForeignKey(OfferColor, verbose_name="Колір", on_delete=models.CASCADE)
    article     = models.CharField(max_length=100, verbose_name="Артикл")
    parameters  = models.ManyToManyField(Parametr, verbose_name="Параметри")
    desc        = models.TextField(verbose_name="Опис російською")
    desc_ua     = models.TextField(verbose_name="Опис українською")
    price       = models.IntegerField(verbose_name="Ціна")
    stock       = models.IntegerField(verbose_name="Кількість")
    images      = models.ManyToManyField(Image, verbose_name="Зображення")
    enable      = models.BooleanField(verbose_name="Статус", default=True)

    def parseModel(self, name):
        name = name.split()
        cleaned_words = []
        for word in name:
            if not any(process.extractOne(word, [exclude], score_cutoff=80) for exclude in EXCLUDES):
                cleaned_words.append(word)

        self.model  = ' '.join(cleaned_words)
        pattern     = re.compile(fr"\b(?:{'|'.join(re.escape(s) for s in SIZES.split())})\b", flags=re.IGNORECASE)
        self.model  = pattern.sub("", self.model).strip()
        self.model  = re.sub(r'\(\d+\)', '',  self.model)   


    def parseType(self, name, deeper = False):
        if True:
            types = [i.name_ua.lower() for i in OfferType.objects.all()]
            if deeper: type_, score = process.extractOne(name.lower().split()[1], types) 
            else: type_, score = process.extractOne(name.lower().split()[0], types)
            if score > 70:
                print(type_)
                self.offer_type = OfferType.objects.get(name_ua=type_.capitalize())
                return True
            else: 
                if not deeper: self.parseType(name, deeper=True)
                else: return False

    def __str__(self) -> str:

        return str(self.offer_type) + " BERSERK SPORT " + str(self.model) + " " + self.color.color_en.lower() + " " + str(self.size) + " (" + self.article + ")"
    


class Gender(Enum):
    MEN     = auto()
    WOMEN   = auto()
    KIDS    = auto()