registry = {}
site_parsers = {}


def warn_overwrite(site, logger=print, target='registry'):
    logger(f'[WARN] Overwriting existing parser for site: "{site}" in {target}')


# def register(site_name, func):
#     registry[site_name] = func

def register(name, func, logger=print):
    if name in registry:
        warn_overwrite(name, logger=logger, target='registry')
    registry[name] = func


def register_site_parser(name, func, logger=print):
    if name in site_parsers:
        warn_overwrite(name, logger=logger, target='site_parsers')
    site_parsers[name] = func


def log_wrapper(func, logger):
    def wrapper(html):
        logger(f"[LOG] BEFORE {func.__name__}")
        result = func(html)
        logger(f"[LOG] AFTER {func.__name__}")
        return result
    return wrapper


def parser(site, debug=False, logger=print):
    if not isinstance(site, str):
        raise TypeError(f'Expected site to be str, got {type(site).__name__}')

    def decorator(func):
        decorated_func = log_wrapper(func, logger) if debug else func
        register_site_parser(site, decorated_func, logger=logger)
        register(site, decorated_func, logger=logger)
        return decorated_func

    return decorator


def log_parse(logger=print):
    def decorator(func):
        return log_wrapper(func, logger)
    return decorator


# def log_parse(logger=print):
#     def decorator(func):
#         def wrapper(html):
#             logger(f'[LOG] BEFORE parsing: {func.__name__}')
#             result = func(html)
#             logger(f'[LOG] AFTER parsing: {func.__name__}')
#             return result
#         return wrapper
#     return decorator