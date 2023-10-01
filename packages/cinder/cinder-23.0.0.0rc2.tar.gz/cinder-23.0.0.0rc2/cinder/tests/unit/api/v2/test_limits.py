# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Tests dealing with HTTP rate-limiting.
"""

from http import client as http_client
import io

from oslo_serialization import jsonutils
import webob

from cinder.api.v2 import limits
from cinder.api import views
import cinder.context
from cinder.tests.unit import test


TEST_LIMITS = [
    limits.Limit("GET", "/delayed", "^/delayed", 1, limits.PER_MINUTE),
    limits.Limit("POST", "*", ".*", 7, limits.PER_MINUTE),
    limits.Limit("POST", "/volumes", "^/volumes", 3, limits.PER_MINUTE),
    limits.Limit("PUT", "*", "", 10, limits.PER_MINUTE),
    limits.Limit("PUT", "/volumes", "^/volumes", 5, limits.PER_MINUTE),
]
NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'ns': 'http://docs.openstack.org/common/api/v1.0',
}


class BaseLimitTestSuite(test.TestCase):
    """Base test suite which provides relevant stubs and time abstraction."""

    def setUp(self):
        super(BaseLimitTestSuite, self).setUp()
        self.time = 0.0
        self.mock_object(limits.Limit, "_get_time", self._get_time)
        self.absolute_limits = {}

        def fake_get_project_quotas(context, project_id, usages=True):
            return {k: dict(limit=v) for k, v in self.absolute_limits.items()}

        self.mock_object(cinder.quota.QUOTAS, "get_project_quotas",
                         fake_get_project_quotas)

    def _get_time(self):
        """Return the "time" according to this test suite."""
        return self.time


class LimitsControllerTest(BaseLimitTestSuite):

    """Tests for `limits.LimitsController` class."""

    def setUp(self):
        """Run before each test."""
        super(LimitsControllerTest, self).setUp()
        self.controller = limits.create_resource()

    def _get_index_request(self, accept_header="application/json"):
        """Helper to set routing arguments."""
        request = webob.Request.blank("/")
        request.accept = accept_header
        request.environ["wsgiorg.routing_args"] = (None, {
            "action": "index",
            "controller": "",
        })
        context = cinder.context.RequestContext('testuser', 'testproject')
        request.environ["cinder.context"] = context
        return request

    def _populate_limits(self, request):
        """Put limit info into a request."""
        _limits = [
            limits.Limit("GET", "*", ".*", 10, 60).display(),
            limits.Limit("POST", "*", ".*", 5, 60 * 60).display(),
            limits.Limit("GET", "changes-since*", "changes-since",
                         5, 60).display(),
        ]
        request.environ["cinder.limits"] = _limits
        return request

    def test_empty_index_json(self):
        """Test getting empty limit details in JSON."""
        request = self._get_index_request()
        response = request.get_response(self.controller)
        expected = {
            "limits": {
                "rate": [],
                "absolute": {},
            },
        }
        body = jsonutils.loads(response.body)
        self.assertEqual(expected, body)

    def test_index_json(self):
        """Test getting limit details in JSON."""
        request = self._get_index_request()
        request = self._populate_limits(request)
        self.absolute_limits = {
            'gigabytes': 512,
            'volumes': 5,
        }
        response = request.get_response(self.controller)
        expected = {
            "limits": {
                "rate": [
                    {
                        "regex": ".*",
                        "uri": "*",
                        "limit": [
                            {
                                "verb": "GET",
                                "next-available": "1970-01-01T00:00:00",
                                "unit": "MINUTE",
                                "value": 10,
                                "remaining": 10,
                            },
                            {
                                "verb": "POST",
                                "next-available": "1970-01-01T00:00:00",
                                "unit": "HOUR",
                                "value": 5,
                                "remaining": 5,
                            },
                        ],
                    },
                    {
                        "regex": "changes-since",
                        "uri": "changes-since*",
                        "limit": [
                            {
                                "verb": "GET",
                                "next-available": "1970-01-01T00:00:00",
                                "unit": "MINUTE",
                                "value": 5,
                                "remaining": 5,
                            },
                        ],
                    },

                ],
                "absolute": {"maxTotalVolumeGigabytes": 512,
                             "maxTotalVolumes": 5, },
            },
        }
        body = jsonutils.loads(response.body)
        self.assertEqual(expected, body)

    def _populate_limits_diff_regex(self, request):
        """Put limit info into a request."""
        _limits = [
            limits.Limit("GET", "*", ".*", 10, 60).display(),
            limits.Limit("GET", "*", "*.*", 10, 60).display(),
        ]
        request.environ["cinder.limits"] = _limits
        return request

    def test_index_diff_regex(self):
        """Test getting limit details in JSON."""
        request = self._get_index_request()
        request = self._populate_limits_diff_regex(request)
        response = request.get_response(self.controller)
        expected = {
            "limits": {
                "rate": [
                    {
                        "regex": ".*",
                        "uri": "*",
                        "limit": [
                            {
                                "verb": "GET",
                                "next-available": "1970-01-01T00:00:00",
                                "unit": "MINUTE",
                                "value": 10,
                                "remaining": 10,
                            },
                        ],
                    },
                    {
                        "regex": "*.*",
                        "uri": "*",
                        "limit": [
                            {
                                "verb": "GET",
                                "next-available": "1970-01-01T00:00:00",
                                "unit": "MINUTE",
                                "value": 10,
                                "remaining": 10,
                            },
                        ],
                    },

                ],
                "absolute": {},
            },
        }
        body = jsonutils.loads(response.body)
        self.assertEqual(expected, body)

    def _test_index_absolute_limits_json(self, expected):
        request = self._get_index_request()
        response = request.get_response(self.controller)
        body = jsonutils.loads(response.body)
        self.assertEqual(expected, body['limits']['absolute'])

    def test_index_ignores_extra_absolute_limits_json(self):
        self.absolute_limits = {'unknown_limit': 9001}
        self._test_index_absolute_limits_json({})


class TestLimiter(limits.Limiter):
    pass


class LimitMiddlewareTest(BaseLimitTestSuite):

    """Tests for the `limits.RateLimitingMiddleware` class."""

    @webob.dec.wsgify
    def _empty_app(self, request):
        """Do-nothing WSGI app."""
        pass

    def setUp(self):
        """Prepare middleware for use through fake WSGI app."""
        super(LimitMiddlewareTest, self).setUp()
        _limits = '(GET, *, .*, 1, MINUTE)'
        self.app = limits.RateLimitingMiddleware(self._empty_app, _limits,
                                                 "%s.TestLimiter" %
                                                 self.__class__.__module__)

    def test_limit_class(self):
        """Test that middleware selected correct limiter class."""
        self.assertIsInstance(self.app._limiter, TestLimiter)

    def test_good_request(self):
        """Test successful GET request through middleware."""
        request = webob.Request.blank("/")
        response = request.get_response(self.app)
        self.assertEqual(http_client.OK, response.status_int)

    def test_limited_request_json(self):
        """Test a rate-limited (413) GET request through middleware."""
        request = webob.Request.blank("/")
        response = request.get_response(self.app)
        self.assertEqual(http_client.OK, response.status_int)

        request = webob.Request.blank("/")
        response = request.get_response(self.app)
        self.assertEqual(http_client.REQUEST_ENTITY_TOO_LARGE,
                         response.status_int)

        self.assertIn('Retry-After', response.headers)
        retry_after = int(response.headers['Retry-After'])
        self.assertAlmostEqual(retry_after, 60, 1)

        body = jsonutils.loads(response.body)
        expected = "Only 1 GET request(s) can be made to * every minute."
        value = body["overLimitFault"]["details"].strip()
        self.assertEqual(expected, value)


class LimitTest(BaseLimitTestSuite):

    """Tests for the `limits.Limit` class."""

    def test_GET_no_delay(self):
        """Test a limit handles 1 GET per second."""
        limit = limits.Limit("GET", "*", ".*", 1, 1)
        delay = limit("GET", "/anything")
        self.assertIsNone(delay)
        self.assertEqual(0, limit.next_request)
        self.assertEqual(0, limit.last_request)

    def test_GET_delay(self):
        """Test two calls to 1 GET per second limit."""
        limit = limits.Limit("GET", "*", ".*", 1, 1)
        delay = limit("GET", "/anything")
        self.assertIsNone(delay)

        delay = limit("GET", "/anything")
        self.assertEqual(1, delay)
        self.assertEqual(1, limit.next_request)
        self.assertEqual(0, limit.last_request)

        self.time += 4

        delay = limit("GET", "/anything")
        self.assertIsNone(delay)
        self.assertEqual(4, limit.next_request)
        self.assertEqual(4, limit.last_request)

    def test_invalid_limit(self):
        """Test that invalid limits are properly checked on construction."""
        self.assertRaises(ValueError, limits.Limit, "GET", "*", ".*", 0, 1)


class ParseLimitsTest(BaseLimitTestSuite):

    """Tests for the default limits parser in the `limits.Limiter` class."""

    def test_invalid(self):
        """Test that parse_limits() handles invalid input correctly."""
        self.assertRaises(ValueError, limits.Limiter.parse_limits,
                          ';;;;;')

    def test_bad_rule(self):
        """Test that parse_limits() handles bad rules correctly."""
        self.assertRaises(ValueError, limits.Limiter.parse_limits,
                          'GET, *, .*, 20, minute')

    def test_missing_arg(self):
        """Test that parse_limits() handles missing args correctly."""
        self.assertRaises(ValueError, limits.Limiter.parse_limits,
                          '(GET, *, .*, 20)')

    def test_bad_value(self):
        """Test that parse_limits() handles bad values correctly."""
        self.assertRaises(ValueError, limits.Limiter.parse_limits,
                          '(GET, *, .*, foo, minute)')

    def test_bad_unit(self):
        """Test that parse_limits() handles bad units correctly."""
        self.assertRaises(ValueError, limits.Limiter.parse_limits,
                          '(GET, *, .*, 20, lightyears)')

    def test_multiple_rules(self):
        """Test that parse_limits() handles multiple rules correctly."""
        try:
            test_limits = limits.Limiter.parse_limits(
                '(get, *, .*, 20, minute);'
                '(PUT, /foo*, /foo.*, 10, hour);'
                '(POST, /bar*, /bar.*, 5, second);'
                '(Say, /derp*, /derp.*, 1, day)')
        except ValueError as e:
            self.assertFalse(str(e))

        # Make sure the number of returned limits are correct
        self.assertEqual(4, len(test_limits))

        # Check all the verbs...
        expected = ['GET', 'PUT', 'POST', 'SAY']
        self.assertEqual(expected, [t.verb for t in test_limits])

        # ...the URIs...
        expected = ['*', '/foo*', '/bar*', '/derp*']
        self.assertEqual(expected, [t.uri for t in test_limits])

        # ...the regexes...
        expected = ['.*', '/foo.*', '/bar.*', '/derp.*']
        self.assertEqual(expected, [t.regex for t in test_limits])

        # ...the values...
        expected = [20, 10, 5, 1]
        self.assertEqual(expected, [t.value for t in test_limits])

        # ...and the units...
        expected = [limits.PER_MINUTE, limits.PER_HOUR,
                    limits.PER_SECOND, limits.PER_DAY]
        self.assertEqual(expected, [t.unit for t in test_limits])


class LimiterTest(BaseLimitTestSuite):

    """Tests for the in-memory `limits.Limiter` class."""

    def setUp(self):
        """Run before each test."""
        super(LimiterTest, self).setUp()
        userlimits = {'limits.user3': '',
                      'limits.user0': '(get, *, .*, 4, minute);'
                                      '(put, *, .*, 2, minute)'}
        self.limiter = limits.Limiter(TEST_LIMITS, **userlimits)

    def _check(self, num, verb, url, username=None):
        """Check and yield results from checks."""
        for x in range(num):
            yield self.limiter.check_for_delay(verb, url, username)[0]

    def _check_sum(self, num, verb, url, username=None):
        """Check and sum results from checks."""
        results = self._check(num, verb, url, username)
        return sum(item for item in results if item)

    def test_no_delay_GET(self):
        """Ensure no delay on a single call for a limit verb we didn't set."""
        delay = self.limiter.check_for_delay("GET", "/anything")
        self.assertEqual((None, None), delay)

    def test_no_delay_PUT(self):
        """Ensure no delay on a single call for a known limit."""
        delay = self.limiter.check_for_delay("PUT", "/anything")
        self.assertEqual((None, None), delay)

    def test_delay_PUT(self):
        """Test delay on 11th PUT request.

        Ensure the 11th PUT will result in a delay of 6.0 seconds until
        the next request will be granced.
        """
        expected = [None] * 10 + [6.0]
        results = list(self._check(11, "PUT", "/anything"))

        self.assertEqual(expected, results)

    def test_delay_POST(self):
        """Test delay on 8th POST request.

        Ensure the 8th POST will result in a delay of 6.0 seconds until
        the next request will be granced.
        """
        expected = [None] * 7
        results = list(self._check(7, "POST", "/anything"))
        self.assertEqual(expected, results)

        expected = 60.0 / 7.0
        results = self._check_sum(1, "POST", "/anything")
        self.assertAlmostEqual(expected, results, 8)

    def test_delay_GET(self):
        """Ensure the 11th GET will result in NO delay."""
        expected = [None] * 11
        results = list(self._check(11, "GET", "/anything"))
        self.assertEqual(expected, results)

        expected = [None] * 4 + [15.0]
        results = list(self._check(5, "GET", "/foo", "user0"))
        self.assertEqual(expected, results)

    def test_delay_PUT_volumes(self):
        """Test delay on /volumes.

        Ensure PUT on /volumes limits at 5 requests, and PUT elsewhere
        is still OK after 5 requests...but then after 11 total requests,
        PUT limiting kicks in.
        """
        # First 6 requests on PUT /volumes
        expected = [None] * 5 + [12.0]
        results = list(self._check(6, "PUT", "/volumes"))
        self.assertEqual(expected, results)

        # Next 5 request on PUT /anything
        expected = [None] * 4 + [6.0]
        results = list(self._check(5, "PUT", "/anything"))
        self.assertEqual(expected, results)

    def test_delay_PUT_wait(self):
        """Test limit is lifted again.

        Ensure after hitting the limit and then waiting for
        the correct amount of time, the limit will be lifted.
        """
        expected = [None] * 10 + [6.0]
        results = list(self._check(11, "PUT", "/anything"))
        self.assertEqual(expected, results)

        # Advance time
        self.time += 6.0

        expected = [None, 6.0]
        results = list(self._check(2, "PUT", "/anything"))
        self.assertEqual(expected, results)

    def test_multiple_delays(self):
        """Ensure multiple requests still get a delay."""
        expected = [None] * 10 + [6.0] * 10
        results = list(self._check(20, "PUT", "/anything"))
        self.assertEqual(expected, results)

        self.time += 1.0

        expected = [5.0] * 10
        results = list(self._check(10, "PUT", "/anything"))
        self.assertEqual(expected, results)

        expected = [None] * 2 + [30.0] * 8
        results = list(self._check(10, "PUT", "/anything", "user0"))
        self.assertEqual(expected, results)

    def test_user_limit(self):
        """Test user-specific limits."""
        self.assertEqual([], self.limiter.levels['user3'])
        self.assertEqual(2, len(self.limiter.levels['user0']))

    def test_multiple_users(self):
        """Tests involving multiple users."""

        # User0
        expected = [None] * 2 + [30.0] * 8
        results = list(self._check(10, "PUT", "/anything", "user0"))
        self.assertEqual(expected, results)

        # User1
        expected = [None] * 10 + [6.0] * 10
        results = list(self._check(20, "PUT", "/anything", "user1"))
        self.assertEqual(expected, results)

        # User2
        expected = [None] * 10 + [6.0] * 5
        results = list(self._check(15, "PUT", "/anything", "user2"))
        self.assertEqual(expected, results)

        # User3
        expected = [None] * 20
        results = list(self._check(20, "PUT", "/anything", "user3"))
        self.assertEqual(expected, results)

        self.time += 1.0

        # User1 again
        expected = [5.0] * 10
        results = list(self._check(10, "PUT", "/anything", "user1"))
        self.assertEqual(expected, results)

        self.time += 1.0

        # User1 again
        expected = [4.0] * 5
        results = list(self._check(5, "PUT", "/anything", "user2"))
        self.assertEqual(expected, results)

        # User0 again
        expected = [28.0]
        results = list(self._check(1, "PUT", "/anything", "user0"))
        self.assertEqual(expected, results)

        self.time += 28.0

        expected = [None, 30.0]
        results = list(self._check(2, "PUT", "/anything", "user0"))
        self.assertEqual(expected, results)


class WsgiLimiterTest(BaseLimitTestSuite):

    """Tests for `limits.WsgiLimiter` class."""

    def setUp(self):
        """Run before each test."""
        super(WsgiLimiterTest, self).setUp()
        self.app = limits.WsgiLimiter(TEST_LIMITS)

    def _request_data(self, verb, path):
        """Get data describing a limit request verb/path."""
        return jsonutils.dump_as_bytes({"verb": verb, "path": path})

    def _request(self, verb, url, username=None):
        """POST request to given url by given username.

        Make sure that POSTing to the given url causes the given username
        to perform the given action.  Make the internal rate limiter return
        delay and make sure that the WSGI app returns the correct response.
        """
        if username:
            request = webob.Request.blank("/%s" % username)
        else:
            request = webob.Request.blank("/")

        request.method = "POST"
        request.body = self._request_data(verb, url)
        response = request.get_response(self.app)

        if "X-Wait-Seconds" in response.headers:
            self.assertEqual(http_client.FORBIDDEN, response.status_int)
            return response.headers["X-Wait-Seconds"]

        self.assertEqual(http_client.NO_CONTENT, response.status_int)

    def test_invalid_methods(self):
        """Only POSTs should work."""
        for method in ["GET", "PUT", "DELETE", "HEAD", "OPTIONS"]:
            request = webob.Request.blank("/", method=method)
            response = request.get_response(self.app)
            self.assertEqual(http_client.METHOD_NOT_ALLOWED,
                             response.status_int)

    def test_good_url(self):
        delay = self._request("GET", "/something")
        self.assertIsNone(delay)

    def test_escaping(self):
        delay = self._request("GET", "/something/jump%20up")
        self.assertIsNone(delay)

    def test_response_to_delays(self):
        delay = self._request("GET", "/delayed")
        self.assertIsNone(delay)

        delay = self._request("GET", "/delayed")
        self.assertEqual('60.00', delay)

    def test_response_to_delays_usernames(self):
        delay = self._request("GET", "/delayed", "user1")
        self.assertIsNone(delay)

        delay = self._request("GET", "/delayed", "user2")
        self.assertIsNone(delay)

        delay = self._request("GET", "/delayed", "user1")
        self.assertEqual('60.00', delay)

        delay = self._request("GET", "/delayed", "user2")
        self.assertEqual('60.00', delay)


class FakeHttplibSocket(object):

    """Fake `http_client.HTTPResponse` replacement."""

    def __init__(self, response_string):
        """Initialize new `FakeHttplibSocket`."""
        if isinstance(response_string, str):
            response_string = response_string.encode('utf-8')
        self._buffer = io.BytesIO(response_string)

    def makefile(self, mode, *args):
        """Returns the socket's internal buffer."""
        return self._buffer


class FakeHttplibConnection(object):

    """Fake `http_client.HTTPConnection`."""

    def __init__(self, app, host):
        """Initialize `FakeHttplibConnection`."""
        self.app = app
        self.host = host

    def request(self, method, path, body="", headers=None):
        """Fake request handler.

        Requests made via this connection actually get translated and
        routed into our WSGI app, we then wait for the response and turn
        it back into an `http_client.HTTPResponse`.
        """
        if not headers:
            headers = {}

        req = webob.Request.blank(path)
        req.method = method
        req.headers = headers
        req.host = self.host
        req.body = body

        resp = str(req.get_response(self.app))
        resp = "HTTP/1.0 %s" % resp
        sock = FakeHttplibSocket(resp)
        self.http_response = http_client.HTTPResponse(sock)
        self.http_response.begin()

    def getresponse(self):
        """Return our generated response from the request."""
        return self.http_response


def wire_HTTPConnection_to_WSGI(host, app):
    """Monkeypatches HTTPConnection.

    Monkeypatches HTTPConnection so that if you try to connect to host, you
    are instead routed straight to the given WSGI app.

    After calling this method, when any code calls

    http_client.HTTPConnection(host)

    the connection object will be a fake.  Its requests will be sent directly
    to the given WSGI app rather than through a socket.

    Code connecting to hosts other than host will not be affected.

    This method may be called multiple times to map different hosts to
    different apps.

    This method returns the original HTTPConnection object, so that the caller
    can restore the default HTTPConnection interface (for all hosts).
    """
    class HTTPConnectionDecorator(object):
        """Decorator to mock the HTTPConecction class.

        Wraps the real HTTPConnection class so that when you instantiate
        the class you might instead get a fake instance.
        """

        def __init__(self, wrapped):
            self.wrapped = wrapped

        def __call__(self, connection_host, *args, **kwargs):
            if connection_host == host:
                return FakeHttplibConnection(app, host)
            else:
                return self.wrapped(connection_host, *args, **kwargs)

    oldHTTPConnection = http_client.HTTPConnection
    new_http_connection = HTTPConnectionDecorator(http_client.HTTPConnection)
    http_client.HTTPConnection = new_http_connection
    return oldHTTPConnection


class WsgiLimiterProxyTest(BaseLimitTestSuite):

    """Tests for the `limits.WsgiLimiterProxy` class."""

    def setUp(self):
        """setUp() for WsgiLimiterProxyTest.

        Do some nifty HTTP/WSGI magic which allows for WSGI to be called
        directly by something like the `http_client` library.
        """
        super(WsgiLimiterProxyTest, self).setUp()
        self.app = limits.WsgiLimiter(TEST_LIMITS)
        oldHTTPConnection = (
            wire_HTTPConnection_to_WSGI("169.254.0.1:80", self.app))
        self.proxy = limits.WsgiLimiterProxy("169.254.0.1:80")
        self.addCleanup(self._restore, oldHTTPConnection)

    def _restore(self, oldHTTPConnection):
        # restore original HTTPConnection object
        http_client.HTTPConnection = oldHTTPConnection

    def test_200(self):
        """Successful request test."""
        delay = self.proxy.check_for_delay("GET", "/anything")
        self.assertEqual((None, None), delay)

    def test_403(self):
        """Forbidden request test."""
        delay = self.proxy.check_for_delay("GET", "/delayed")
        self.assertEqual((None, None), delay)

        delay, error = self.proxy.check_for_delay("GET", "/delayed")
        error = error.strip()

        expected = ("60.00",
                    b"403 Forbidden\n\nOnly 1 GET request(s) can be "
                    b"made to /delayed every minute.")

        self.assertEqual(expected, (delay, error))


class LimitsViewBuilderTest(test.TestCase):
    def setUp(self):
        super(LimitsViewBuilderTest, self).setUp()
        self.view_builder = views.limits.ViewBuilder()
        self.rate_limits = [{"URI": "*",
                             "regex": ".*",
                             "value": 10,
                             "verb": "POST",
                             "remaining": 2,
                             "unit": "MINUTE",
                             "resetTime": 1311272226},
                            {"URI": "*/volumes",
                             "regex": "^/volumes",
                             "value": 50,
                             "verb": "POST",
                             "remaining": 10,
                             "unit": "DAY",
                             "resetTime": 1311272226}]
        self.absolute_limits = {"gigabytes": 1,
                                "backup_gigabytes": 2,
                                "volumes": 3,
                                "snapshots": 4,
                                "backups": 5}

    def test_build_limits(self):
        tdate = "2011-07-21T18:17:06"
        expected_limits = {
            "limits": {"rate": [{"uri": "*",
                                 "regex": ".*",
                                 "limit": [{"value": 10,
                                            "verb": "POST",
                                            "remaining": 2,
                                            "unit": "MINUTE",
                                            "next-available": tdate}]},
                                {"uri": "*/volumes",
                                 "regex": "^/volumes",
                                 "limit": [{"value": 50,
                                            "verb": "POST",
                                            "remaining": 10,
                                            "unit": "DAY",
                                            "next-available": tdate}]}],
                       "absolute": {"maxTotalVolumeGigabytes": 1,
                                    "maxTotalBackupGigabytes": 2,
                                    "maxTotalVolumes": 3,
                                    "maxTotalSnapshots": 4,
                                    "maxTotalBackups": 5}}}

        output = self.view_builder.build(self.rate_limits,
                                         self.absolute_limits)
        self.assertDictEqual(expected_limits, output)

    def test_build_limits_empty_limits(self):
        expected_limits = {"limits": {"rate": [],
                           "absolute": {}}}

        abs_limits = {}
        rate_limits = []
        output = self.view_builder.build(rate_limits, abs_limits)
        self.assertDictEqual(expected_limits, output)
