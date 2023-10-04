import shortuuid


class AddSilicaPageIdToRequest:
    """If not already set, add a _silica_page_id to the request object. This helps with defining active components in the cache."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "_silicia_page_session_id" not in request.META:
            request.META["_silicia_page_session_id"] = shortuuid.uuid()

        return self.get_response(request)
