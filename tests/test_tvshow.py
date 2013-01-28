from pytvdb.model.tv_show import TVShow
from pytvdb.model.exceptions import TVDBException

import os
from nose.tools import assert_raises

def test_tvshow_basic():
    xml = open(os.path.join(os.getcwd(),os.sep.join(['tests','inputs','en.xml'])),'r').read()
    t = TVShow.from_xml(xml)
    assert isinstance(t.actors,list)
    assert len(t.seasons) ==4
    assert len(t.seasons[1])==7

def test_tvshow_withart():
    xml = open(os.path.join(os.getcwd(),os.sep.join(['tests','inputs','en.xml'])),'r').read()
    banner = open(os.path.join(os.getcwd(),os.sep.join(['tests','inputs','banners.xml'])),'r').read()
    t = TVShow.from_xml(series=xml,art=banner)
    assert isinstance(t.actors,list)
    assert len(t.seasons) ==4
    assert t.seasons[1].cover_art!=None
    assert t.seasons[1].cover_art.banner_path==u'seasons/78859-2.jpg'
