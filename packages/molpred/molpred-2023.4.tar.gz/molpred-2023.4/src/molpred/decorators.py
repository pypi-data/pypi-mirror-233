#!/usr/bin/env python3
'''
Decorators
'''


def caching_method(method):
    '''
    Decorator for a caching instance method that will re-use previous results
    when invoked with the same arguments. The equivalency is checked with the
    "is" operator complex types with the same value will still be considered
    different by the decorated method.


    Args:
        method:
            The instance method to wrap.

    Returns:
        The decorated instance method.
    '''
    name = method.__name__
    cache_name = f'_{name}_cache'

    def cmethod(self, *args, **kwargs):
        input_ids = [str(id(arg)) for arg in args]
        input_ids.extend(
            f'{key}:{id(value)}'
            for (key, value) in sorted(kwargs.items())
        )
        identifier = '\n'.join(input_ids)

        try:
            cache = getattr(self, cache_name)
        except AttributeError:
            cache = {}
            setattr(self, cache_name, cache)

        try:
            return cache[identifier]
        except KeyError:
            result = method(self, *args, **kwargs)
            cache[identifier] = result
            return result

    cmethod.__doc__ = method.__doc__
    return cmethod


def caching_class(cls):
    '''
    Decorator for classes with caching methods decorated with @caching_method.
    This will add a "clear_caches" method that clears each caching methods
    private cache.

    Args:
        cls:
            A class containing methods decorated with @caching_method.

    Returns:
        The decorated class with a new "clear_caches" method for clearing the
        internal caches.
    '''
    def clear_caches(self):
        for name, value in self.__dict__:
            if name.startswith('_') and name.endswith('_cache') and isinstance(value, dict):
                value.clear()

    cls.clear_caches = clear_caches
    return cls
