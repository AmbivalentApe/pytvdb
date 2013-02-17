from abc import ABCMeta
import urllib

class TVDBShowProvider:
    __metaclass__ = ABCMeta

    def get_show(name,language='en',strict=False):
        raise NotImplemented

    def search(name,language='en',strict=False):
        raise NotImplemented
    
    def get_show_by_imdbid(imdbid):
        raise NotImplemented
    
    def get_show_by_zap2itid(zap2itid):
        raise NotImplemented
    
    def get_episode(series,air_date,language='en'):
        raise NotImplemented


def http_get(url):
    """
    Internal search method. Given tvdb.com sometimes struggles under load,
    maintain internal state and retry for 5 times before giving up.
    """
    retries = 5
    last_exception = None
    while retries > 0:
        try:
            response = urllib.urlopen(url)
            response = response.read()
            return response
        except IOError as e:
            logger.exception(e)
            retries = retries-1
            last_exception = e # track this so we can rethrow it
    raise TVDBException(last_exception)

