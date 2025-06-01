registry = {}

def register(site_name, func):
    registry[site_name] = func


# def register_parser(site_name):
#     if not isinstance(site_name, str):
#         raise TypeError(f'Site name must be a string, got {type(site_name).__name__}')

#     def decorator(func):
#         # Optional: Warn if overwriting existing key
#         if site_name in registry:
#             print(f'[WARN] Overwriting existing parser for site: "{site_name}"')

#         registry[site_name] = func
#         return func
#     return decorator


# def log_parse(func):
#     def wrapper(html):
#         print(f'[LOG] BEFORE parsing: {func.__name__}')
#         result = func(html)
#         print(f'[LOG] AFTER parsing: {func.__name__}')
#         return result
#     return wrapper

def log_parse(logger=print):
    def decorator(func):
        def wrapper(html):
            logger(f'[LOG] BEFORE parsing: {func.__name__}')
            result = func(html)
            logger(f'[LOG] AFTER parsing: {func.__name__}')
            return result
        return wrapper
    return decorator