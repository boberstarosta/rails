class Event(list):
    def fire(self, *args, **kwargs):
        for callback in self:
            callback(*args, **kwargs)
    
    __call__ = fire
