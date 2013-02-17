from .model.episode import Episode
from .model.exceptions import TVDBException
from .model.tv_show import TVShow
from .impl import TVDBShowProvider

# the underlying implementation
__impl__ = None

def _bootstrap(provider=None,**kwargs):
    '''
    internal bootstrap function 
   
    if provider is not specified, it defaults to the internal HttpTVDBAdapter,
    else it is assumed (for now) that you are passing in an implementation of TVDBShowProvider
    '''
    global __impl__
    if provider is None:
        from .impl.basic import HttpTVDBAdapter
        __impl__ = HttpTVDBAdapter()
    else:
        __impl__ = provider

def search(name,language='en',strict=False):
    """
    Public search function.
    
    Returns a list of items that match the value of name
    """
    global __impl__
    if __impl__ is None:
        _bootstrap()

    results = __impl__.search(name,language)
    return results

def get_details(show,language='en'):
    '''
    Return information on the given show
    '''
    global __impl__
    
    if __impl__ is None:
        _bootstrap()

    return __impl__.get_show(show,language)
