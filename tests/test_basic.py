from pytvdb.impl.basic import HttpTVDBAdapter
from pytvdb.model.exceptions import TVDBException
from pytvdb.model.episode import Episode
from nose.tools import assert_raises
from datetime import date
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

def test_search():
    adapter = HttpTVDBAdapter()
    assert len(adapter.search(r"I don't exist, honest"))==0
    results = adapter.search('90210')
    print results
    assert len(results)==3
    results = adapter.search('Ashes to Ashes')
    print results
    assert len(results)==3

    results = adapter.search('Ashes to Ashes',strict=True)
    print results
    assert len(results)==1

def test_get_and_parse():
    adapter = HttpTVDBAdapter()
    with assert_raises(TVDBException) as cm:
        tv_show = adapter.get_show(r"I don't exist, honest")
    assert "No series found for \"I don't exist, honest\"" == str(cm.exception)
    
    with assert_raises(TVDBException) as cm:
        tv_show = adapter.get_show(r"Ashes")
    assert "Multiple series found for \"Ashes\"" == str(cm.exception)
    
    tv_show = adapter.get_show('Unit One')
    assert isinstance(tv_show.actors,list)
    assert tv_show.id == 78859
    assert tv_show.seasons[1].cover_art!=None
    assert tv_show.seasons[1].cover_art.banner_path==u'seasons/78859-2.jpg'

def test_externalids():
    adapter = HttpTVDBAdapter()
    with assert_raises(TVDBException) as cm:
        episode = adapter.get_show_by_imdbid(-1)
    print cm.exception
    assert "No series found for \"imdbid=-1\"" == str(cm.exception)
    show = adapter.get_show_by_imdbid('tt0290978')
    assert show.id == 78107

def test_episode_by_airdate():
    adapter = HttpTVDBAdapter()
    with assert_raises(TVDBException) as cm:
        episode = adapter.get_episode(r"I don't exist, honest",date(2000,10,01))
    assert "No series found for \"I don't exist, honest\"" == str(cm.exception)
     
    with assert_raises(TVDBException) as cm:
        episode = adapter.get_episode(r"90210",date(2000,10,10))
    assert "Multiple series found for \"90210\"" == str(cm.exception)
    
    with assert_raises(TVDBException) as cm:
        episode = adapter.get_episode(-1,-1)
    assert "air_date must be a datetime.date" == str(cm.exception)
    
    with assert_raises(TVDBException) as cm:
        episode = adapter.get_episode(-1,date(2000,10,01))
    assert "No episode found" == str(cm.exception)
    
    episode = adapter.get_episode('Unit One',date(2000,10,01))
    assert isinstance(episode,Episode)
    print episode.__dict__
    assert episode.episode_name == u"Assistance Report A-15/99"
