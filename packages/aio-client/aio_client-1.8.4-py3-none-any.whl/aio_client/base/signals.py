# coding: utf-8
import functools

import django.dispatch


# Сигнал - получение всех данных завершено
get_data_done = django.dispatch.Signal()


def robust_sender(signal, **kwargs):
    """
    Декоратор отправки сигнала методом send_robust. Не учитывает
    возможность отправки аргументов сигнала::

        @robust_sender(get_data_done, sender=GetProviderRequest)
        def data_getter():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            result, is_send_signal = func(*a, **kw)
            if is_send_signal:
                signal.send_robust(**kwargs)
            return result
        return wrapper
    return decorator
