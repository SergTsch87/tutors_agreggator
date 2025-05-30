registry = {}

def register(site_name, func):
    registry[site_name] = func


def register_parser(site_name):
    if not isinstance(site_name, str):
        raise TypeError(f'Site name must be a string, got {type(site_name).__name__}')

    def decorator(func):
        registry[site_name] = func
        return func
    return decorator