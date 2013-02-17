from lxml import etree
from .exceptions import TVDBException
from . import TVDBType,convert_to_map, convert_to_pythonic_form

class Poster(TVDBType):
    def __init__(self,**kwargs):
        for item in kwargs.keys():
            setattr(self,convert_to_pythonic_form(item),kwargs[item])

        self._convert_field(['season','id'],int)
        self._art_enriched = False

    def __str__(self):
        return "Poster:{%s}" % (str(self.__dict__))


    def enrich_art(self):
        if not self._art_enriched:
            if hasattr(self,'banner_path') and self.banner_path is not None:
                self.banner_path = self._get_art(self.banner_path)
            if hasattr(self,'thumbnail_path') and self.thumbnail_path is not None:
                self.banner_path = self._get_art(self.thumbnail_path)
            self._art_enriched = True
                
            
   

    @staticmethod
    def from_xml(xml):
        args = convert_to_map(xml,u'Banner')
        return Poster(**args)
 
