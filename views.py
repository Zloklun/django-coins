#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache, cache_control

from .models import *


CACHE_SEC = 60 * 60
MAX_AGE = 60 * 60


def _ctx(ctx):
    ctx.update({'CACHE_SEC': CACHE_SEC})
    return ctx


def jsonify(q):
    return serialize('json', q)


def index(request):
    return render(request, 'index_coins.html', _ctx({'title': 'Главная страница'}))


def all_coins(request):
    coins = Coin.objects.all().select_related('mint', 'currency__country')
    return render(request, 'coins.html', _ctx({'title': 'Все монеты', 'coins': coins}))


def all_coins_json(request):
    return JsonResponse({
        'title': 'Все монеты',
        'currencies': jsonify(Currency.objects.all()),
        'countries': jsonify(Country.objects.all()),
        'mints': jsonify(Mint.objects.all()),
        'coins': jsonify(Coin.objects.all()),
        'series': jsonify(Series.objects.all()),
    })


def rubles(request):
    russia = Country.objects.get(short_name='РФ').id
    coins = Coin.objects.filter(currency__country_id=russia).select_related('mint', 'currency__country', 'series')
    return render(request, 'coins.html', _ctx({
        'title': 'Современные монеты России',
        'coins': coins,
        'single_country': True,
    }))


def foreigns(request):
    russia = Country.objects.get(short_name='РФ').id
    coins = Coin.objects.exclude(currency__country_id=russia).select_related('mint', 'currency__country', 'series')
    return render(request, 'coins.html', _ctx({
        'title': 'Монеты других стран',
        'coins': coins,
        'single_country': False,
    }))
