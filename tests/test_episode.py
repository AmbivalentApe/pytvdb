from pytvdb.model.episode import Episode
from pytvdb.model.exceptions import TVDBException

from nose.tools import assert_raises

def test_parse_wrongtype():
    with assert_raises(TVDBException) as cm:
        Episode.from_xml(1)
    assert 'Unrecognised type for xml input <type \'int\'> must be one of str, lxml.etree' == str(cm.exception)

def test_parse_invalidxml():
    with assert_raises(TVDBException) as cm:
        Episode.from_xml('<dfdf></erer>')
    assert 'Error parsing Episode XML' in str(cm.exception)
    with assert_raises(TVDBException) as cm:
        Episode.from_xml('<dfdf></dfdf>')
    assert 'Root node is not an Episode' in str(cm.exception)

def test_episode():
    import os
    xml = open(os.path.join(os.getcwd(),os.sep.join(['tests','inputs','episode.xml'])),'r').read()
    e = Episode.from_xml(xml)
    print e
    assert e.episode_number ==2
    assert len(e.guest_stars) == 8
