import functools

def methodcache(f):
    """Utility decorator that ensures the passed function is only called once and the result 
    is cached and reused on future calls. This saves the cached values in the method __cache
    attribute (only works for methods).
    """

    name = f.__name__

    @functools.wraps(f)
    def cached(self, *args, **kwargs):
        if not hasattr(self, "__cache"):
            self.__cache = {}

        if name not in self.__cache:
            self.__cache[name] = {"called": False, "result": None}

        if self.__cache[name]["called"]:
            return self.__cache[name]["result"]

        result = f(self, *args, **kwargs)
        self.__cache[name] = {"called": True, "result": result}
        return result

    return cached
