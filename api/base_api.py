class BaseAPI:
    """Base class for all apis."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items(): 
            setattr(self, key, value)


    def crawl(self):
        return False


    def get(self):
        raise NotImplementedError


