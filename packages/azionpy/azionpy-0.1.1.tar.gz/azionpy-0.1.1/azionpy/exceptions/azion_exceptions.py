"""Exceptions used to describe errors when handling
Azion API requests/responses.
"""


class AzionException(Exception):
    """Base class exception. All exceptions related to
    requests/responses errors are inherited from it.
    """
    pass


class InternalError(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)


class AzionError(AzionException):

    def __init__(self, response):
        super().__init__(self, response)
        self.response = response
        self.status_code = response.status_code
        self.errors = response.json()

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.status_code}]>'


class BadRequest(AzionError):
    """Indicate that the server could not understand the request due
    to invalid syntax.

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
    """
    pass


class Unauthorized(AzionError):
    """Indicate that the request has not been applied because it lacks
    valid authentication credentials for the target resource.

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401
    """
    pass


class Forbidden(AzionError):
    """Indicate that the server understood the request but refuses to
    authorize it.

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403
    """
    pass


class NotFound(AzionError):
    """Indicate that the server can't find the requested resource.
    Links which lead to a 404 page are often called broken or dead links.

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
    """
    pass


class MethodNotAllowed(AzionError):
    """Indicate that the request method is known by the server
    but has been disabled and cannot be used.

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405
    """
    pass


class NotAcceptable(AzionError):
    """Indicate that a response matching the list of acceptable values
    defined in Accept-Charset and Accept-Language cannot be served.

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
    """
    pass


class Conflict(AzionError):
    """Indicate a request conflict with current state of the server.
    """
    pass


class TooManyRequests(AzionError):
    """Indicate he user has sent too many requests
    in a given amount of time ("rate limiting").

    More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429
    """
    pass


error_handlers = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    406: NotAcceptable,
    409: Conflict,
    429: TooManyRequests
}


def handle_error(response):
    """Handle the request that failed to retrieve an appropriate
    response.

    :param object response:
        requests Response object.
    """
    handler = error_handlers.get(response.status_code)
    return handler(response)