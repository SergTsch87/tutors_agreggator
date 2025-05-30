registry = {}

def register(site_name, func):
    registry[site_name] = func