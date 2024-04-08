import os
import functools

def do_not_run_in_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        test = os.environ.get('ENV')
        if os.environ.get('ENV') != 'test':
            return func(*args, **kwargs)
    return wrapper
    
def create_all_directories():
    create_latency_directory()
    create_success_directory()
    create_log_directory()

def create_latency_directory():
    os.makedirs("./Plots/Latency")

def create_success_directory():
    os.makedirs("./Plots/Success")

def create_log_directory():
    os.makedirs("./Logs")

def create_log_file():
    os.makedirs("./log.txt")
