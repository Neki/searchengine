class RequestDocument:

    def __init__(self, request):
        self.request = request

    def get_full_text(self):
        return self.request

    @property
    def doc_id(self):
        return -1

