import requests
from django.conf import settings
from django.core.cache import cache
from collections import defaultdict

# Порядок дней недели для группировки
DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def format_schedule(sch: dict) -> str:
    # если есть готовый текст
    if 'text' in sch and sch['text']:
        return sch['text']
    # иначе собираем по дням
    by_day = {}
    for day in DAY_NAMES:
        info = sch.get(day, {})
        wh = info.get('working_hours', [])
        if wh:
            times = ', '.join(f"{h['from']}–{h['to']}" for h in wh)
            by_day[day] = times
        else:
            by_day[day] = '—'

    # группируем подряд идущие дни с одинаковым расписанием
    groups = []
    prev_t = None
    start = None
    for day in DAY_NAMES + [None]:
        t = by_day.get(day) if day else None
        if t != prev_t:
            if prev_t is not None:
                groups.append((start, prev_day, prev_t))
            start = day
            prev_t = t
        prev_day = day

    # форматируем
    parts = []
    for a, b, t in groups:
        if not a or not b:
            continue
        if a == b:
            parts.append(f"{a}: {t}")
        else:
            parts.append(f"{a}–{b}: {t}")
    return '; '.join(parts)


def external_restaurants(
    query: str='ресторан',
    radius: int=5000,
    lat: float=43.238949,
    lon: float=76.889709,
    limit: int=50,
    cache_ttl: int=3600,
):
    cache_key = f"2gis:{query}:{lat}:{lon}:{radius}:{limit}"
    data = cache.get(cache_key)
    if data is not None:
        return data

    url = 'https://catalog.api.2gis.com/3.0/items'
    results = []
    page, batch = 1, 10

    while len(results) < limit:
        sz = min(limit - len(results), batch)
        params = {
            'q'         : query,
            'point'     : f'{lon},{lat}',
            'radius'    : radius,
            'page_size' : sz,
            'page'      : page,
            'fields'    : (
                'items.point,'
                'items.address_name,'
                'items.address_comment,'
                'items.phones,'
                'items.schedule,'
                'items.www,'
                'items.rating,'
                'items.purpose_name,'
                'items.type,'
                'items.cover'
            ),
            'key'       : settings.DGIS_API_KEY,
        }
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        items = resp.json().get('result', {}).get('items', [])
        if not items:
            break

        for it in items:
            sch = it.get('schedule') or {}
            results.append({
                'name'           : it.get('name',''),
                'address'        : it.get('address_name',''),
                'address_comment': it.get('address_comment',''),
                'phone'          : (it.get('phones') or [{}])[0].get('phone',''),
                'hours'          : format_schedule(sch),
                'is_24x7'        : sch.get('is_24x7', False),
                'website'        : (it.get('www') or [{}])[0].get('value',''),
                'rating'         : it.get('rating'),
                'purpose_name'   : it.get('purpose_name',''),
                'type'           : it.get('type',''),
                'avatar_url'     : (it.get('cover') or {}).get('url',''),
                'lat'            : (it.get('point') or {}).get('lat'),
                'lon'            : (it.get('point') or {}).get('lon'),
            })

        if len(items) < sz:
            break
        page += 1

    data = results[:limit]
    cache.set(cache_key, data, cache_ttl)
    return data
