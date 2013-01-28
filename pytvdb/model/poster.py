from lxml import etree
from .exceptions import TVDBException
from . import TVDBType,convert_to_map, convert_to_pythonic_form

class Poster(TVDBType):
    def __init__(self,**kwargs):
        for item in kwargs.keys():
            setattr(self,convert_to_pythonic_form(item),kwargs[item])

        self._convert_field(['season','id'],int)

    def __str__(self):
        return "Poster:{%s}" % (str(self.__dict__))

    @staticmethod
    def from_xml(xml):
        args = convert_to_map(xml,'Banner')
        return Poster(**args)
 
