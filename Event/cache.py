from django.core.cache import cache


def get_cached(cache_key, queryset, timeout: int = 30):
    cached = cache.get(cache_key)
    if cached is None:
        cached = list(queryset)
        cache.set(cache_key, cached, timeout)
    return cached
