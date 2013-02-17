from . import TVDBType
from .exceptions import TVDBException
class Season(TVDBType):
    def __init__(self,episodes,cover_art=None):
        i_dict = {}
        seasons = [e.season_number for e in episodes]
        if len(set(seasons))> 1:
            raise TVDBException(message='Season numbers not unique in input list (%s)' % (str(seasons)))
        
        for e in episodes:
            i_dict[e.episode_number] = e
        self._episodes = i_dict 
        episode_numbers = i_dict.keys()
        episode_numbers.sort()
        self._episode_numbers = episode_numbers
        self.cover_art = cover_art
        self._art_enriched = False


    def enrich_art(self):
        if not self._art_enriched:
            for e in self._episodes.values():
                e.enrich_art()
            self._art_enriched = True

    def __len__(self):
        return len(self._episode_numbers)

    def __iter__(self):
        for e in self._episode_numbers:
            yield self._episodes[e]
    
    def __getitem__(self,key):
        return self._episodes[key] 
