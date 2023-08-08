import functools
import datetime
import json
def do_twice(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper

def debug(func):
    """Выводит сигнатуру функции и возвращаемое значение"""
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Вызываем {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} вернула значение - {value!r}")
        return value
    return wrapper_debug

def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        with open('logs.txt', 'a') as f:
            f.write(f'[DATETIME: {datetime.datetime.now()}]\n')
            f.write('======= REQUEST =======\n')
            f.write(f'{func.__name__}\n')
            f.write(f'Url: {res.request.url}\n')
            f.write(f'Path: {res.request.path_url}\n')
            f.write(f'Headers: {res.request.headers}\n')
            f.write(f'Method: {res.request.method}\n')
            f.write(f'Data: {res.request.body}\n\n')

            f.write('======= RESPONSE =======\n')
            f.write(f'Status Code: {res.status_code}\n')
            f.write(f'Data: {result}\n\n')

        return res
    return wrapper