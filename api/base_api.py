class BaseAPI:
    """Base class for all apis."""

    def __init__(self, auth, bucket):
        self.auth = auth
        self.bucket = bucket


    def crawl(self):
        return False


    def get(self):
        raise NotImplementedError


