#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Coin(models.Model):
    '''A coin'''
    face_value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name='Номинал',
    )
    currency = models.ForeignKey(
        'Currency',
        verbose_name='Валюта',
    )
    year = models.DecimalField(
        decimal_places=0,
        max_digits=4,
        verbose_name='Год выпуска',
    )
    mint = models.ForeignKey(
        'Mint',
        blank=True,
        null=True,
        verbose_name='Монетный двор',
    )
    series = models.ForeignKey(
        'Series',
        blank=True,
        null=True,
        verbose_name='Серия',
    )
    series_item = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Название в серии',
    )
    country = models.ForeignKey(
        'Country',
        blank=True,
        verbose_name='Страна обращения',
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий',
    )
    magnetic = models.BooleanField(
        default=False,
        verbose_name='Магнитная'
    )
    count = models.IntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self):
        s = ''
        if self.currency.symbol:
            s = '{}{} {}, {}'.format(
                 self.face_value,
                 self.currency.symbol,
                 self.country.short_name,
                 self.year)
        else:
            s = '{} {} {}, {}'.format(
                 self.face_value,
                 self.currency.name,
                 self.country.short_name,
                 self.year)
        if self.series:
            s += ' ({})'.format(self.series.short_name, self.series_item)
        return s

    def save(self):
        try:
            assert self.country is not None
        except ObjectDoesNotExist:
            self.country = self.currency.country
        super(Coin, self).save()

    class Meta:
        verbose_name = 'Монета'
        verbose_name_plural = 'Монеты'
        ordering = (
            'currency__name',
            'face_value',
            'year',
            'series__name',
            'series_item',
        )


class Mint(models.Model):
    '''Mint'''
    name = models.CharField(max_length=50, verbose_name='Название')
    tag = models.CharField(max_length=10, verbose_name='Сокращённое название')
    country = models.ForeignKey('Country', verbose_name='Страна')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Монетный двор'
        verbose_name_plural = 'Монетные дворы'
        ordering = ('country', 'name')


class Series(models.Model):
    '''Coin series'''
    name = models.CharField(max_length=75, verbose_name='Название')
    short_name = models.CharField(max_length=25, verbose_name='Краткое название')
    country = models.ForeignKey('Country', verbose_name='Страна')

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Серия монет'
        verbose_name_plural = 'Серии монет'


class Currency(models.Model):
    '''Currency'''
    name = models.CharField(max_length=50, verbose_name='Название')
    small_name = models.CharField(  # Name for fractions
        max_length=50,
        verbose_name='Название дробной части'
    )
    code = models.CharField(max_length=3, verbose_name='Код ISO 4217')
    symbol = models.CharField(
        max_length=3,
        verbose_name='Символ',
        blank=True,
        null=True
    )
    country = models.ForeignKey('Country', verbose_name='Страна-эмитент')
    exists = models.BooleanField(default=True, verbose_name='Ещё выпускается')

    def __str__(self):
        return '{} {}'.format(self.name, self.country.short_name)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Country(models.Model):
    '''Country'''
    name = models.CharField(max_length=50, verbose_name='Полное название')
    short_name = models.CharField(max_length=25, verbose_name='Сокращённое название')
    code = models.CharField(max_length=2, verbose_name='Код ISO 3166-1')
    flag = models.ImageField(verbose_name='Флаг страны')
    exists = models.BooleanField(
        default=True,
        verbose_name='Страна ещё существует',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class CatalogueEntry(models.Model):
    '''CatalogueEntry'''
    coin = models.ForeignKey('Coin', verbose_name='Монета', related_name='catalogueentries')
    catalogue = models.ForeignKey('Catalogue', verbose_name='Каталог')
    number = models.CharField(max_length=15, verbose_name='Каталожный номер')

    def __str__(self):
        return self.catalogue.name + ' ' + self.number

    class Meta:
        verbose_name = 'Каталожная запись'
        verbose_name_plural = 'Каталожные записи'
        ordering = ('catalogue', 'number')


class Catalogue(models.Model):
    '''Catalogue'''
    name = models.CharField(max_length=50, verbose_name='Название')
    short_name = models.CharField(max_length=5, verbose_name='Короткое название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
