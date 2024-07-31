from django.db import models
from django.contrib.auth.views import get_user_model

User = get_user_model()

class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True



class Material(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    PRICE_FOR = (
        ("METR_KV", 'метр.кв'),
        ("THINGS", 'шт'),
        ("METER_KUB", 'м.куб'),
        ("KILOGRAM", "кг"),
        ("LITR", "литр")
    )
    CURRENCY = (
        ("DOLLAR", 'доллар'),
        ("EURO", 'эвро'),
        ("COM", 'сом')
    )

    name = models.CharField(verbose_name="Навзвание материала", max_length=200)
    description = models.TextField(verbose_name="Описание материла подробно")
    category = models.ForeignKey("stroy.Category",verbose_name="Выберите категорию товара", on_delete=models.PROTECT)
    company = models.ForeignKey("stroy.Company", verbose_name="Выберите компанию", on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name="Цена")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField("Валюта", choices=CURRENCY, max_length=20)
    price_for = models.CharField("Цена за", choices=PRICE_FOR, max_length=20)
    tags = models.ManyToManyField('stroy.Tags', related_name="nfts", verbose_name="Выберите теги")
    viewing = models.IntegerField("Просмотры", editable=False, null=True, blank=True)
    favorites = models.IntegerField("Избранные", editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.name}"



class Company(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    user = models.ForeignKey(User, verbose_name="Выберите пользователя", on_delete=models.CASCADE, related_name="company")
    name = models.CharField("Название компании", max_length=100)
    description = models.TextField(verbose_name="Описание компании")
    adres = models.CharField(max_length=100, verbose_name="Адрес компании")

    def __str__(self):
        return f"{self.name}"



class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField("Название категории", max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    


class Images(models.Model):

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображении'

    material = models.ForeignKey('stroy.Material', related_name='images', on_delete=models.CASCADE, verbose_name="Выберите материал")
    image = models.ImageField('Изображение', upload_to='material_images/')


class Tags(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    name = models.CharField(verbose_name="Название тега", max_length=100)
    def __str__(self) -> str:
        return f'{self.name}'

# Create your models here.
