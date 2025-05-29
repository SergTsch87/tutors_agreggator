def log_parse(func):
    def wrapper(*args, **kwargs):
        print('Starting parsing...')
        result = func(*args, **kwargs)
        print('Parsing done.')
        return result
    
    return wrapper


@log_parse
def parse_example():
    print('Parsing something...')