class Event(list):
    def fire(self, sender, *args, **kwargs):
        for callback in self:
            callback(sender, *args, **kwargs)
    
    __call__ = fire
