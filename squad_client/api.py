import requests
import logging
import urllib
import re


url_validator_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

logger = logging.getLogger('api')


class ApiException(requests.exceptions.RequestException):
    pass


class SquadApi:
    url = None
    token = None
    headers = None

    @staticmethod
    def configure(url, token=None):
        if url_validator_regex.match(url) is None:
            raise ApiException('Malformed url: "%s"' % url)

        if token:
            SquadApi.token = token
            SquadApi.headers = {"Authorization": 'token %s' % token}

        SquadApi.url = url if url[-1] is '/' else url + '/'
        logger.debug('SquadApi: url = "%s" and token = "%s"' % (SquadApi.url, 'yes' if SquadApi.token else 'no'))

    @staticmethod
    def get(endpoint, params):
        if endpoint.startswith('http'):
            parsed_url = urllib.parse.urlparse(endpoint)
            assert SquadApi.url == '%s://%s/' % (parsed_url.scheme, parsed_url.netloc), \
                   'Given url (%s) is does not match pre-configured one!'

            params.update(urllib.parse.parse_qs(parsed_url.query))
            endpoint = parsed_url.path

        url = '%s%s' % (SquadApi.url, endpoint if endpoint[0] is not '/' else endpoint[1:])
        logger.debug('GET %s (%s)' % (url, params))
        return requests.get(url=url, params=params, headers=SquadApi.headers)

