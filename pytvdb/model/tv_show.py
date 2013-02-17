from lxml import etree
from .exceptions import TVDBException
from . import TVDBType,parse_xml,convert_to_map, convert_to_pythonic_form
from .episode import Episode
from .poster import Poster
from .season import Season

class TVShow(TVDBType):
    def __init__(self,**kwargs):
        for item in kwargs.keys():
            if item not in ['seasons','episodes','art']:
                setattr(self,convert_to_pythonic_form(item),kwargs[item])

        self._convert_field(['id','seasonid'],int)
        self._convert_field(['actors'],list)
        season_art = {}
        if 'art' in kwargs:
            self.fan_art = [X for X in kwargs['art'] if X.banner_type=='fanart']
            series_art = [X for X in kwargs['art'] if X.banner_type=='series']
            if len(series_art)==1:
                series_art=series_art[0]
            self.series_art = series_art
            season_art = {X.season:X for X in kwargs['art'] if X.banner_type=='season'}
            self.season_art = season_art

        if 'seasons' in kwargs:
            self.seasons = kwargs['seasons']
        elif 'episodes' in kwargs:
            episodes = kwargs['episodes']
            seasons = set([int(e.season_number) for e in episodes])
            seasons = list(seasons)
            seasons.sort()
            series = [Season([X for X in episodes if int(X.season_number) ==i],season_art.get(i,None)) for i in seasons]
            self.seasons = series
        self._art_enriched = False

    def enrich_art(self):
        if not self._art_enriched:
            attributes = ['fan_art','series_art','banner','season_art']
            for attr in attributes:
                print attr
                if hasattr(self,attr) and getattr(self,attr) is not None:
                    val = getattr(self,attr)
                    if isinstance(val,str):
                        setattr(self,attr,self._get_art(val))
                    elif isinstance(val,list):
                        for X in val:
                            if isinstance(X,TVDBType):
                                X.enrich_art()
            self.seasons.enrich_art()
            self._art_enriched = True

            
    def __str__(self):
        return "TVShow{%s}" % (self.__dict__)

    @staticmethod
    def from_xml(series,art=None):
        args = parse_xml(series,'Data')
        kargs = convert_to_map(args.xpath('Series')[0])
        episodes = [Episode.from_xml(X) for X in args.xpath('Episode')]
        kargs['episodes'] = episodes
        if art!=None:
            art = parse_xml(art,'Banners')
            art = [Poster.from_xml(X) for X in art.xpath('Banner')]
            kargs['art'] = art
        return TVShow(**kargs)        
 
