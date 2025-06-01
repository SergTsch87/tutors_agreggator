registry = {}

def register(site_name, func):
    registry[site_name] = func


def log_parse(logger=print):
    def decorator(func):
        def wrapper(html):
            logger(f'[LOG] BEFORE parsing: {func.__name__}')
            result = func(html)
            logger(f'[LOG] AFTER parsing: {func.__name__}')
            return result
        return wrapper
    return decorator