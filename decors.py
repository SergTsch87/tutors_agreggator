registry = {}

def register(site_name, func):
    registry[site_name] = func


def register_parser(site_name):
    def decorator(func):
        registry[site_name] = func
        return func
    return decorator