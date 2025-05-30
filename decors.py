def log_parse(func):
    def wrapper(*args, **kwargs):
        print('Starting parsing...')
        result = func(*args, **kwargs)
        print('Parsing done.')
        return result
    
    return wrapper