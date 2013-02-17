from pytvdb.model.poster import Poster
from pytvdb.model.exceptions import TVDBException
from lxml import etree
from nose.tools import assert_raises
import os
'''
Not much to do here, poster is a pretty simple class
'''
def test_posters():
    xml = etree.fromstring(open(os.path.join(os.getcwd(),os.sep.join(['tests','inputs','banners.xml'])),'r').read())
    image = open(os.path.join(os.getcwd(),os.sep.join(['tests','inputs','78859-1.jpg'])),'rb').read()
    e = Poster.from_xml(xml.xpath('Banner')[0])
    print e
    assert e.id==769461 # check the id is being mapped to int
    assert e.banner_path==u'fanart/original/78859-1.jpg'
    e.enrich_art()
    assert e.banner_path == image
