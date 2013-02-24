from .model.episode import Episode
from .model.exceptions import TVDBException
from .model.tv_show import TVShow
from .impl import TVDBShowProvider
from .configuration import bootstrap
import os
__author__ = 'Phil Anderson'
__versioninfo__ = (0, 1, 0)
__version__ = '.'.join(map(str, __versioninfo__))

# the underlying implementation
__impl__ = None


       
def search(name,language='en',strict=False):
    """
    Public search function.
    
    Returns a list of items that match the value of name
    """
    global __impl__
    if __impl__ is None:
        __impl__ = bootstrap()

    results = __impl__.search(name,language)
    return results

def get_details(show,language='en'):
    '''
    Return information on the given show
    '''
    global __impl__
    
    if __impl__ is None:
        __impl__ = bootstrap()

    return __impl__.get_show(show,language)
