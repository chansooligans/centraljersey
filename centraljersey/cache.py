from glob import glob

import pandas as pd

reload = False


def localcache(
    name=None, dtype=None, fp_out="/home/chansoo/projects/centraljersey/data"
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if name:
                filename = f"{fp_out}/{name}"
            else:
                filename = f"{fp_out}/{func.__name__}.csv"

            if (filename in glob(f"{fp_out}/*")) & (reload == False):
                df = pd.read_csv(filename, dtype=dtype)
            else:
                df = func(*args, **kwargs)
                df.to_csv(filename, index=False)
            return df

        return wrapper

    return decorator
