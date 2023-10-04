
from prometheus_api_client import PrometheusConnect, PrometheusApiClientException


class PrometheusApiClient(PrometheusConnect):
    """
    A Class from a Prometheus Host.

    :param url: (str) url for the prometheus host
    :param headers: (dict) A dictionary of http headers to be used to communicate with
        the host. Example: {"Authorization": "bearer my_oauth_token_to_the_host"}
    :param disable_ssl: (bool) If set to True, will disable ssl certificate verification
        for the http requests made to the prometheus host
    :param retry: (Retry) Retry adapter to retry on HTTP errors
    """

    def __init__(self, url: str = "http://127.0.0.1:9090", headers: dict = None, disable_ssl: bool = False, retry=None):
        super().__init__(url, headers, disable_ssl, retry)


    def all_alerts(self, params: dict = None):
        """
        Get the list of all the alerts that the prometheus host scrapes.

        :param params: (dict) Optional dictionary containing GET parameters to be
            sent along with the API request, such as "time"
        :returns: (list) A list of names of all the alerts available from the
            specified prometheus host
        :raises:
            (RequestException) Raises an exception in case of a connection error
            (PrometheusApiClientException) Raises in case of non 200 response status code
        """
        params = params or {}
        response = self._session.get(
            "{0}/api/v1/rules".format(self.url),
            verify=self.ssl_verification,
            headers=self.headers,
            params=params,
        )

        if response.status_code == 200:
            self._all_alerts = response.json()["data"]
        else:
            raise PrometheusApiClientException(
                "HTTP Status Code {} ({!r})".format(response.status_code, response.content)
            )
        return self._all_alerts


