def __before(preparation):
    def decorator(func):
        def applicator(*args, **kwargs):
            preparation()
            return func(*args, **kwargs)

        return applicator

    return decorator
