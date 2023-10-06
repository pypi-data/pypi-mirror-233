from importlib.metadata import version

falcon_major_version = int(version("falcon")[0])

import falcon
from falcon_crossorigin import (
    CrossOrigin,
    DEFAULT_METHODS,
    HEADER_ACCEPT,
    HEADER_ACCESS_CONTROL_ALLOW_ORIGIN,
    HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS,
    HEADER_ACCESS_CONTROL_ALLOW_HEADERS,
    HEADER_ACCESS_CONTROL_ALLOW_METHODS,
    HEADER_ACCESS_CONTROL_EXPOSE_HEADERS,
    HEADER_ACCESS_CONTROL_MAX_AGE,
    HEADER_ACCESS_CONTROL_REQUEST_METHOD,
    HEADER_ACCESS_CONTROL_REQUEST_HEADERS,
    HEADER_ORIGIN,
    HEADER_VARY,
)

from . import base

JOINER = ", "
if falcon.__version__[0] == "1":
    JOINER = ","


class TestCrossOrigin(base.TestBase):
    def setUp(self, cross_origin=None):
        super(TestCrossOrigin, self).setUp(cross_origin)
        self.entry_path = "/"

    def tearDown(self):
        super(TestCrossOrigin, self).tearDown()

    def override_settings(self, **kwargs):
        self.setUp(CrossOrigin(**kwargs))

    def test_request_defaults(self):
        self.simulate_get(self.entry_path)

        self.assertEqual("*", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN])
        self.assertEqual(HEADER_ORIGIN, self.res_headers[HEADER_VARY])

    def test_request_expose_headers(self):
        self.override_settings(expose_headers="Link")

        self.simulate_get(self.entry_path)

        self.assertEqual("Link", self.res_headers[HEADER_ACCESS_CONTROL_EXPOSE_HEADERS])

    def test_request_custom_settings(self):
        methods = "GET,POST"
        headers = "Pragma,Expires,Cache-Control"
        expose = "Link"
        self.override_settings(
            allow_origins="localhost",
            allow_methods=methods,
            allow_headers=headers,
            allow_credentials=True,
            expose_headers=expose,
            max_age=3600,
        )

        self.simulate_get(self.entry_path, headers={HEADER_ORIGIN: "localhost"})

        self.assertEqual(
            "true", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS]
        )
        self.assertEqual(
            "localhost", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN]
        )
        self.assertEqual(expose, self.res_headers[HEADER_ACCESS_CONTROL_EXPOSE_HEADERS])
        self.assertEqual(HEADER_ORIGIN, self.res_headers[HEADER_VARY])

    def test_preflight_defaults(self):
        self.simulate_options(self.entry_path)

        self.assertEqual("*", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN])
        self.assertEqual(
            DEFAULT_METHODS, self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_METHODS]
        )
        res_headers = [
            HEADER_ORIGIN,
            HEADER_ACCESS_CONTROL_REQUEST_METHOD,
            HEADER_ACCESS_CONTROL_REQUEST_HEADERS,
        ]
        if falcon_major_version > 2:
            res_headers.insert(0, HEADER_ACCEPT)
        self.assertEqual(JOINER.join(res_headers), self.res_headers[HEADER_VARY])

    def test_preflight_allow_origins(self):
        self.override_settings(allow_origins="localhost")

        self.simulate_get(self.entry_path, headers={HEADER_ORIGIN: "localhost"})
        self.assertEqual(
            "localhost", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN]
        )

    def test_preflight_allow_methods(self):
        methods = "GET,POST"
        self.override_settings(allow_methods=methods)

        self.simulate_options(self.entry_path)

        self.assertEqual(methods, self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_METHODS])

    def test_preflight_allow_credentials(self):
        self.override_settings(allow_credentials=True)

        self.simulate_options(self.entry_path)

        self.assertEqual(
            "true", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS]
        )

    def test_preflight_allow_headers(self):
        headers = "Pragma,Expires,Cache-Control"
        self.override_settings(allow_headers=headers)

        self.simulate_options(self.entry_path)

        self.assertEqual(headers, self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_HEADERS])

    def test_preflight_request_headers(self):
        headers = "Pragma,Expires,Cache-Control"

        self.simulate_options(
            self.entry_path, headers={HEADER_ACCESS_CONTROL_REQUEST_HEADERS: headers}
        )

        self.assertEqual(headers, self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_HEADERS])

    def test_preflight_max_age(self):
        self.override_settings(max_age=3600)

        self.simulate_options(self.entry_path)

        self.assertEqual("3600", self.res_headers[HEADER_ACCESS_CONTROL_MAX_AGE])

    def test_preflight_custom_settings(self):
        methods = "GET,POST"
        headers = "Pragma,Expires,Cache-Control"
        expose = "Link"
        self.override_settings(
            allow_origins="localhost",
            allow_methods=methods,
            allow_headers=headers,
            allow_credentials=True,
            expose_headers=expose,
            max_age=3600,
        )

        self.simulate_options(self.entry_path, headers={HEADER_ORIGIN: "localhost"})

        self.assertEqual(
            "true", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_CREDENTIALS]
        )
        self.assertEqual(methods, self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_METHODS])
        self.assertEqual(
            "localhost", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN]
        )
        self.assertEqual("3600", self.res_headers[HEADER_ACCESS_CONTROL_MAX_AGE])
        self.assertEqual(headers, self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_HEADERS])
        vary = [
            HEADER_ORIGIN,
            HEADER_ACCESS_CONTROL_REQUEST_METHOD,
            HEADER_ACCESS_CONTROL_REQUEST_HEADERS,
        ]
        if falcon_major_version > 2:
            vary.insert(0, HEADER_ACCEPT)
        self.assertEqual(JOINER.join(vary), self.res_headers[HEADER_VARY])

    def test_preflight_wildcard_origin(self):
        self.override_settings(
            allow_origins="*",
            allow_credentials=True,
        )

        self.simulate_options(self.entry_path, headers={HEADER_ORIGIN: "localhost"})

        self.assertEqual(
            "localhost", self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN]
        )

    def test_preflight_wildcard_origin_sub_domain(self):
        self.override_settings(allow_origins="https://*.example.com")

        self.simulate_options(
            self.entry_path,
            headers={
                HEADER_ORIGIN: "https://aaa.example.com",
            },
        )

        self.assertEqual(
            "https://aaa.example.com",
            self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN],
        )

        self.simulate_options(
            self.entry_path,
            headers={
                HEADER_ORIGIN: "https://bbb.example.com",
            },
        )

        self.assertEqual(
            "https://bbb.example.com",
            self.res_headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN],
        )
