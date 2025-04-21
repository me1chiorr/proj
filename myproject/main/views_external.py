# main/views_external.py

import requests
from django.conf import settings

def external_restaurants():
    """
    Возвращает список ресторанов из 2ГИС в формате list of dicts.
    """
    point    = '43.238949,76.889709'           # Алматы
    radius   = 5000                            # радиус в метрах
    category = '27100000003634803'             # ID категории «рестораны»
    key      = settings.DGIS_API_KEY

    url = (
        'https://catalog.api.2gis.com/3.0/catalog/branch/search'
        f'?point={point}&radius={radius}&categories={category}'
        '&fields=items.name,items.address,items.point,items.tel,items.schedule'
        f'&key={key}'
    )

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        items = resp.json().get('result', {}).get('items', [])
    except Exception as e:
        print('Ошибка 2ГИС API:', e)
        items = []

    # Преобразуем «сырые» объекты в удобные словари
    return [
        {
            'id':      item.get('id'),
            'name':    item.get('name'),
            'address': item.get('address', {}).get('name', ''),
            'lat':     item.get('point', {}).get('lat'),
            'lon':     item.get('point', {}).get('lon'),
            'phone':   item.get('tel',   [{}])[0].get('value', ''),
            'hours':   item.get('schedule', {}).get('week'),
        }
        for item in items
    ]
