import datetime

from django.db import models

# Create your models here.


class MoneyAdditionNote(models.Model):
    date_created = models.DateField(
        verbose_name='Дата создания записи', blank=True, null=True)
    status = models.ForeignKey(
        'MoneyAdditionStatus', related_name='status_notes', blank=False,
        verbose_name='Статус', on_delete=models.CASCADE)
    money_type = models.ForeignKey(
        'MoneyAdditionType', related_name='type_notes', blank=False,
        verbose_name='Тип', on_delete=models.CASCADE)
    category = models.ForeignKey(
        'MoneyAdditionCategory', related_name='category_notes', blank=False,
        verbose_name='Категория', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        'MoneyAdditionSubCategory', related_name='subcategory_notes',
        verbose_name='Подкатегория', blank=False, on_delete=models.CASCADE)
    money_value = models.DecimalField(
        verbose_name='Сумма в рублях', max_digits=10, decimal_places=2)
    comment = models.TextField(
        verbose_name='Комментарий', blank=True, null=True, max_length=256)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Запись движения денежных средств)'
        verbose_name_plural = 'Записи движения денежных средств'

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.date.today()
        super().save(*args, **kwargs)


class MoneyAdditionStatus(models.Model):
    name = models.CharField(verbose_name='Наименование статуса', max_length=120)
    slug = models.SlugField(
        verbose_name="Slug", max_length=255, blank=True, db_index=True,
        help_text='Нужен для обращения к элементам. Генерируется автоматически',
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Статус движения денежных средств'
        verbose_name_plural = 'Статусы движения денежных средств'

    def __str__(self):
        return self.name


class MoneyAdditionType(models.Model):
    name = models.CharField(verbose_name='Наименование типа', max_length=120)
    slug = models.SlugField(
        verbose_name="Slug", max_length=255, blank=True, db_index=True,
        help_text='Нужен для обращения к элементам. Генерируется автоматически',
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип движения денежных средств'
        verbose_name_plural = 'Типы движения денежных средств'

    def __str__(self):
        return self.name


class MoneyAdditionCategory(models.Model):
    name = models.CharField(
        verbose_name='Наименование категории', max_length=120)
    money_type = models.ForeignKey(
        'MoneyAdditionType', related_name='categories', verbose_name='Тип',
        blank=False, on_delete=models.CASCADE)
    slug = models.SlugField(
        verbose_name="Slug", max_length=255, blank=True, db_index=True,
        help_text='Нужен для обращения к элементам. Генерируется автоматически',
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория движения денежных средств'
        verbose_name_plural = 'Категории движения денежных средств'

    def __str__(self):
        return self.name


class MoneyAdditionSubCategory(models.Model):
    name = models.CharField(
        verbose_name='Наименование подкатегории', max_length=120)
    money_category = models.ForeignKey(
        'MoneyAdditionCategory', related_name='subcategories',
        verbose_name='Категория', blank=False, on_delete=models.CASCADE)
    slug = models.SlugField(
        verbose_name="Slug", max_length=255, blank=True, db_index=True,
        help_text='Нужен для обращения к элементам. Генерируется автоматически',
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Подкатегория движения денежных средств'
        verbose_name_plural = 'Подкатегории движения денежных средств'

    def __str__(self):
        return self.name

