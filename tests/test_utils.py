from pytvdb.model import convert_to_pythonic_form

def test_propertyname():
    assert convert_to_pythonic_form('EpisodeName') == 'episode_name'
    assert convert_to_pythonic_form(' Episode Name') == 'episode_name'
