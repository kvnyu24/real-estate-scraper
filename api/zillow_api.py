class ZillowAPI:
    """Base class for all apis."""

    def __init__(self, params):
        self.params = params


    def crawl(self):
        return False


    def get(self):
        raise NotImplementedError


