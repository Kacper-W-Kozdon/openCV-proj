from functools import wraps


def region_wrapper(func):
    def outer(_self, **kwargs):
        region_name = kwargs.get("region_name")

        @wraps(func)
        def inner(*args, **kwargs):
            return func(_self, region_name=region_name)

        return inner

    return outer
