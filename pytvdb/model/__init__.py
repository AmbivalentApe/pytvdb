from lxml import etree
from .exceptions import TVDBException

def parse_xml(xml,root_name):
    '''
    Uitlity function for parsing xml into an lxml.etree
    '''
    if isinstance(xml,str):
        try:
            xml = etree.fromstring(xml)
        except etree.XMLSyntaxError as e:
            raise TVDBException(message='Error parsing %s XML (%s) ' % (root_name,e.message))
    elif not isinstance(xml,etree._Element):
        raise TVDBException(message='Unrecognised type for xml input %s must be one of str, lxml.etree' % (type(xml)))

    if root_name!=None and xml.tag!=root_name:
        raise TVDBException(message = 'Root node is not an %s (%s)' % (root_name,xml.tag))
    return xml

def convert_to_map(xml,tag_name=None,convert_property_names=False):
    xml = parse_xml(xml,tag_name)
    if convert_property_names:
        return {convert_to_pythonic_form(X.tag):unicode(X.text) for X in xml.getchildren()}
    else:
        return {X.tag:unicode(X.text) for X in xml.getchildren()}

def convert_to_pythonic_form(property_name):
    '''
    Convert strings to a more pythonic form better suited for attribute names (eg FirstAired becomes first_aired.
    '''
    def rep(match):
        return '_'+match.group(0).lower()
    import re

    # first convert all upper case characters to _lowercase
    property_name = re.sub('[A-Z]+',rep,property_name)
    # now replace all spaces with underscores
    property_name = re.sub('\ +','_',property_name)
    # tidy up any multiple underscores
    property_name = re.sub('_+','_',property_name)
    if property_name[0]=='_':
        return property_name[1:]
    else:
        return property_name 

from abc import ABCMeta
class TVDBType:
    __metaclass__ = ABCMeta

    def enrich_art(self):
        '''
        Resolve any images if appropriate
        '''
        pass

    def _convert_field(self,fields,new_type):
        ''' 
        Utility function for remapping all of the object atributes in fields to the new_type
        New types available are int and list
        '''
        for field in fields:
            if hasattr(self,field):
                val = getattr(self,field)
                if val=='None':
                    setattr(self,field,None)
                    continue
                if val is not None:
                    if new_type == int:
                        setattr(self,field,int(val))
                    if new_type ==list:
                        setattr(self,field,[unicode(X) for X in val.split('|') if X !=''])  
