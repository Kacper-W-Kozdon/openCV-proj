from functools import wraps


def region_wrapper(func):
    def outer(_self, **kwargs):
        region_name = kwargs.get("region_name") or "region1"
        select_frame_or_points = kwargs.get("select_frame_or_points") or "frame"

        @wraps(func)
        def inner(*args, **kwargs):
            return func(
                _self,
                region_name=region_name,
                select_frame_or_points=select_frame_or_points,
            )

        return inner

    return outer
