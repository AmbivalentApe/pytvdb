from pytvdb.impl.basic import HttpTVDBAdapter
from pytvdb.model.exceptions import TVDBException
from nose.tools import assert_raises
import os

_ENVVAR_NAME='TVDBAPPLICATIONID' 

def test_noid():
    appid = None
    with assert_raises(TVDBException) as cm:
        if _ENVVAR_NAME in os.environ:
            appid = os.environ.pop(_ENVVAR_NAME)
        HttpTVDBAdapter()
    if appid!=None:
        os.environ[_ENVVAR_NAME] = appid
    assert 'application_id is None and TVDBAPPLICATIONID is not set' == str(cm.exception)


def test_fetch_and_parse():
    adapter = HttpTVDBAdapter()
    tv_show = adapter.get_show('Unit One')
    assert isinstance(tv_show.actors,list)
    assert tv_show.id == 78859
    assert tv_show.seasons[1].cover_art!=None
    assert tv_show.seasons[1].cover_art.banner_path==u'seasons/78859-2.jpg'

