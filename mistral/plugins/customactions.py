"""
Collection of Mistral custom actions
"""

from oslo_log import log as logging
import requests
import six
import json as json_lib
from mistral import exceptions as exc
from mistral_lib import actions

LOG = logging.getLogger(__name__)


class HTTPAction(actions.Action):
    """Custom HTTP action. Default std.http action throws error if status-code not in range of (200, 307). This custom
    action add additional status-codes for success. Below is the list additional status-codes.
    - 409 Conflict (useful to continue next task if resource already exists instead throwing error)


    :param url: URL for the new HTTP request.
    :param method: (optional, 'GET' by default) method for the new HTTP
        request.
    :param params: (optional) Dictionary or bytes to be sent in the
        query string for the HTTP request.
    :param body: (optional) Dictionary, bytes, or file-like object to send
        in the body of the HTTP request.
    :param json: (optional) A JSON serializable Python object to send
        in the body of the HTTP request.
    :param headers: (optional) Dictionary of HTTP Headers to send with
        the HTTP request.
    :param cookies: (optional) Dict or CookieJar object to send with
        the HTTP request.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom
        HTTP Auth.
    :param timeout: (optional) Float describing the timeout of the request
        in seconds.
    :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE
        redirect following is allowed.
    :param proxies: (optional) Dictionary mapping protocol to the URL of
        the proxy.
    :param verify: (optional) if ``True``, the SSL cert will be verified.
        A CA_BUNDLE path can also be provided.
    """

    def __init__(self,
                 url,
                 method="GET",
                 params=None,
                 body=None,
                 json=None,
                 headers=None,
                 cookies=None,
                 auth=None,
                 timeout=None,
                 allow_redirects=None,
                 proxies=None,
                 verify=None):
        super(HTTPAction, self).__init__()

        if auth and len(auth.split(':')) == 2:
            self.auth = (auth.split(':')[0], auth.split(':')[1])
        else:
            self.auth = auth

        if isinstance(headers, dict):
            for key, val in headers.items():
                if isinstance(val, (six.integer_types, float)):
                    headers[key] = str(val)

        if body and json:
            raise exc.ActionException(
                "Only one of the parameters 'json' and 'body' can be passed"
            )

        self.url = url
        self.method = method
        self.params = params
        self.body = json_lib.dumps(body) if isinstance(body, dict) else body
        self.json = json
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.verify = verify

    def run(self, context):
        LOG.info(
            "Running HTTP action "
            "[url=%s, method=%s, params=%s, body=%s, json=%s,"
            " headers=%s, cookies=%s, auth=%s, timeout=%s,"
            " allow_redirects=%s, proxies=%s, verify=%s]",
            self.url,
            self.method,
            self.params,
            self.body,
            self.json,
            self.headers,
            self.cookies,
            self.auth,
            self.timeout,
            self.allow_redirects,
            self.proxies,
            self.verify
        )

        try:
            url_data = six.moves.urllib.parse.urlsplit(self.url)
            if 'https' == url_data.scheme:
                action_verify = self.verify
            else:
                action_verify = None

            resp = requests.request(
                self.method,
                self.url,
                params=self.params,
                data=self.body,
                json=self.json,
                headers=self.headers,
                cookies=self.cookies,
                auth=self.auth,
                timeout=self.timeout,
                allow_redirects=self.allow_redirects,
                proxies=self.proxies,
                verify=action_verify
            )
        except Exception as e:
            LOG.exception(
                "Failed to send HTTP request for action execution: %s",
                context.execution.action_execution_id
            )
            raise exc.ActionException("Failed to send HTTP request: %s" % e)

        LOG.info(
            "HTTP action response:\n%s\n%s",
            resp.status_code,
            resp.content
        )

        # Represent important resp data as a dictionary.
        try:
            content = resp.json(encoding=resp.encoding)
        except Exception:
            LOG.debug("HTTP action response is not json.")
            content = resp.content
            if content and resp.encoding not in (None, 'utf-8'):
                content = content.decode(resp.encoding).encode('utf-8')

        _result = {
            'content': content,
            'status': resp.status_code,
            'headers': dict(resp.headers.items()),
            'url': resp.url,
            'history': resp.history,
            'encoding': resp.encoding,
            'reason': resp.reason,
            'cookies': dict(resp.cookies.items()),
            'elapsed': resp.elapsed.total_seconds()
        }

        if resp.status_code not in range(200, 307) or resp.status_code not in (409,):
            return actions.Result(error=_result)

        return _result

    def test(self, context):
        # TODO(rakhmerov): Implement.
        return None
