from functools import wraps

def tag(key=None, modes=[], **kwargs):

    def _tag(func):
        @wraps(func)
        def inner(self, *args, **kwargs): 
            return func(self, *args, **kwargs)
        inner.key=key
        inner.func=func
        inner.modes=modes
        inner.tagged=True
        inner.kwargs=kwargs
        inner.name=func.__name__
        return inner
    return _tag
