#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import *


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    '''CoinAdmin'''
    list_display = (
        'face_value',
        'year',
        'currency',
        'magnetic',
        'mint',
        'series',
        'series_item',
        'count',
    )
    search_fields = (
        '^face_value',
        '^year',
        'country__name',
        'country__short_name',
        'country__code',
        'country__exists',
        'currency__name',
        '=currency__code',
        '=currency__symbol',
        'series__name',
        '=series__short_name',
        'mint__name',
        'mint__tag',
    )

    actions = ('make_magnetic', 'make_diamagnetic')

    def make_magnetic(self, request, queryset):
        '''Mark coins as magnetic'''
        print(request.POST)
        queryset.update(magnetic=True)
    make_magnetic.short_description = 'Пометить магнитными'

    def make_diamagnetic(self, request, queryset):
        '''Mark coins as diamagnetic'''
        print(request.POST)
        queryset.update(magnetic=False)
    make_diamagnetic.short_description = 'Пометить немагнитными'


@admin.register(Mint)
class MintAdmin(admin.ModelAdmin):
    '''MintAdmin'''
    pass


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    '''SeriesAdmin'''
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    '''CurrencyAdmin'''
    list_display = ('name', 'exists', 'country')
    search_fields = ('name', 'symbol', 'country__name', 'country__short_name')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    '''CountryAdmin'''
    list_display = ('name', 'exists')
    search_fields = ('name', 'short_name')


@admin.register(CatalogueEntry)
class CatalogueEntryAdmin(admin.ModelAdmin):
    '''CatalogueEntryAdmin'''
    list_display = ('catalogue', 'number', 'coin')


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    '''CatalogueAdmin'''
    list_display = ('name', )
    search_fields = ('@name', )
