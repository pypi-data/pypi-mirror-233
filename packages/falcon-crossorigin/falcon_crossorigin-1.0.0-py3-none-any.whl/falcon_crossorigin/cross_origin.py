import falcon

from .header import (
    HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS,
    HEADER_ACCESS_CONTROL_ALLOW_HEADERS,
    HEADER_ACCESS_CONTROL_ALLOW_METHODS,
    HEADER_ACCESS_CONTROL_ALLOW_ORIGIN,
    HEADER_ACCESS_CONTROL_EXPOSE_HEADERS,
    HEADER_ACCESS_CONTROL_MAX_AGE,
    HEADER_ACCESS_CONTROL_REQUEST_HEADERS,
    HEADER_ACCESS_CONTROL_REQUEST_METHOD,
    HEADER_ORIGIN,
    HEADER_VARY,
)
from .method import (
    DEFAULT_METHODS,
    METHOD_OPTIONS,
)
from .util import _match_sub_domain


class CrossOrigin:
    def __init__(
        self,
        allow_origins: str = "*",
        allow_methods: str = DEFAULT_METHODS,
        allow_headers: str = "",
        allow_credentials: bool = False,
        expose_headers: str = "",
        max_age: bool = 0,
    ):
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.allow_credentials = allow_credentials
        self.expose_headers = expose_headers
        self.max_age = max_age

    def process_response(
        self,
        req,
        resp,
        resource,
        req_succeeded,
    ):
        origin = req.get_header(HEADER_ORIGIN, default="")
        allow_origin = ""

        for o in self.allow_origins.split(","):
            if o == "*" and self.allow_credentials:
                allow_origin = origin
                break
            if o == "*" or o == origin:
                allow_origin = o
                break
            if _match_sub_domain(origin, o):
                allow_origin = origin
                break

        # Request
        if req.method != METHOD_OPTIONS:
            resp.set_header(HEADER_VARY, HEADER_ORIGIN)
            resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_ORIGIN, allow_origin)
            if self.allow_credentials:
                resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS, "true")
            if self.expose_headers != "":
                resp.set_header(
                    HEADER_ACCESS_CONTROL_EXPOSE_HEADERS, self.expose_headers
                )
            return

        # Preflight request
        resp.append_header(HEADER_VARY, HEADER_ORIGIN)
        resp.append_header(HEADER_VARY, HEADER_ACCESS_CONTROL_REQUEST_METHOD)
        resp.append_header(HEADER_VARY, HEADER_ACCESS_CONTROL_REQUEST_HEADERS)
        resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_ORIGIN, allow_origin)
        resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_METHODS, self.allow_methods)

        if self.allow_credentials:
            resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS, "true")
        if self.allow_headers != "":
            resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_HEADERS, self.allow_headers)
        else:
            h = req.get_header(HEADER_ACCESS_CONTROL_REQUEST_HEADERS, default="")
            if h != "":
                resp.set_header(HEADER_ACCESS_CONTROL_ALLOW_HEADERS, h)
        if self.max_age > 0:
            resp.set_header(HEADER_ACCESS_CONTROL_MAX_AGE, self.max_age)

        resp.status = falcon.HTTP_NO_CONTENT
