
import os

def picklecache(match_args=True, reset=False):
    """Caching method that pickles arguments and return values for a given
    function and saves them for reuse across multiple runs of the same program.

    Args:
        match_args (bool, optional): if True, only returns the cached value if 
            args and kwargs match those saved. Otherwise, returns the value regardless.

        reset (bool, optional): if True, resets the cache and doesn't load saved values.
    """

    def real_decorator(f):
        import pickle
        import functools

        def dump(path, args, kwargs, data):
            with open(path, "wb") as f:
                d = {"args" : args, "kwargs" : kwargs, "data" : data}
                pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
        
        if not os.path.exists(".picklecache"):
            os.mkdir(".picklecache")

        if reset:
            path = os.path.join(".picklecache", "{}".format(f.__name__))

            if os.path.exists(path):
                os.remove(path)
        
        @functools.wraps(f)  
        def wrapper(*args, **kwargs):
            path = os.path.join(".picklecache", "{}".format(f.__name__))

            if os.path.exists(path):
                try:
                    with open(path, "rb") as pfile:
                        cache = pickle.load(pfile)

                    if match_args:
                        cached_args = cache["args"]
                        cached_kwargs = cache["kwargs"]

                        if args == cached_args and kwargs == cached_kwargs:
                            print("Loading data from cache for function {}".format(f.__name__))
                            return cache["data"]

                        else:
                            data = f(*args, **kwargs)
                            dump(path, args, kwargs, data)
                            return data
                    else:
                        print("Loading data from cache for function {}".format(f.__name__))
                        return cache["data"]

                except Exception as e:
                    print("Corrupted pickle cache. Resetting cache for function {}".format(f.__name__))
                    if os.path.exists(path):
                        os.remove(path)

                    retval = f(*args, **kwargs)
                    dump(path, args, kwargs, retval)
                    return retval

            else:
                retval = f(*args, **kwargs)
                dump(path, args, kwargs, retval)
                return retval
        return wrapper

    return real_decorator