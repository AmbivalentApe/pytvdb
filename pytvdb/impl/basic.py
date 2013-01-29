from zipfile import ZipFile
import StringIO
from lxml import etree
import urllib
from ..model.tv_show import TVShow
from ..model.exceptions import TVDBException
from . import TVDBShowProvider
import os
'''


'''

class HttpTVDBAdapter(TVDBShowProvider):


    def __init__(self,application_id=None,base_url='http://www.thetvdb.com/api/',):
        if application_id is None:
            if 'TVDBAPPLICATIONID' not in os.environ:
                raise TVDBException(message='application_id is None and TVDBAPPLICATIONID is not set')
            self.application_id = os.environ['TVDBAPPLICATIONID']
        else:
            self.application_id = application_id
        self.base_url = base_url
        
    def get_show(self,name,language='en'):
        GET_SERIES='GetSeries.php?seriesname='
        series_info = urllib.urlopen(self.base_url+GET_SERIES+urllib.quote_plus(name))
        series_xml = etree.fromstring(series_info.read())
        series_id = series_xml.xpath('//seriesid')[0].text

        base_zip = '%s%s/series/%s/all/%s.zip' % (self.base_url,self.application_id,series_id,language)
        print base_zip
        base_zip = urllib.urlopen(base_zip).read()

        zip_stream = StringIO.StringIO()
        zip_stream.write(base_zip)
        base_zip = ZipFile(zip_stream)

        episodes = base_zip.open(language+'.xml').read()
        art = base_zip.open('banners.xml').read()
        meta_info = TVShow.from_xml(episodes,art)
        return meta_info
