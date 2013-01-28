from pytvdb.model.episode import Episode
from pytvdb.model.season import Season
from pytvdb.model.exceptions import TVDBException

from nose.tools import assert_raises


'''
Check that passing in a non homogenous set of seasoned episodes errors
'''
def test_mismatched():
    with assert_raises(TVDBException) as cm:
        Season([Episode(**{'season_number':1}),Episode(**{'season_number':2})])
    assert 'Season numbers not unique in input list ([1, 2])' == str(cm.exception)

'''
Test behaviour of the collection itself
First check accessors work as expected.
'''
def test_collection():
    s = Season([Episode(**{'season_number':1,'episode_number':1}),Episode(**{'season_number':1,'episode_number':0})])
    assert len(s)==2
    assert s[1] !=None
    assert s[0] !=None
    with assert_raises(KeyError) as cm:
        assert s[2] != None

    episodes = [e.episode_number for e in s]
    assert episodes == [0,1]
