import os
import functools

def do_not_run_in_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.environ.get('ENV') != 'test':
            return func(*args, **kwargs)
    return wrapper