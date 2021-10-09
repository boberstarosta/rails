class Event(list):
    def fire(self, *args, **kwargs):
        for callback in self:
            callback(*args, **kwargs)
    
    __call__ = fire


track_node_created = Event()
track_node_moved = Event()
track_nodes_connected = Event()
