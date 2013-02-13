from zipfile import ZipFile
import StringIO
from lxml import etree
import urllib
from ..model.tv_show import TVShow
from ..model.episode import Episode
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
        series_info = self._get(self.base_url+GET_SERIES+urllib.quote_plus(name)+'&language='+language)
        series_xml = etree.fromstring(series_info)
        series_id = series_xml.xpath('//seriesid')
        if len(series_id)==0:
            raise TVDBException("No series found for \"%s\"" % (name))
        elif len(series_id)>1: 
            raise TVDBException("Multiple series found for \"%s\"" % (name))
        series_id = series_id[0].text

        base_zip = '%s%s/series/%s/all/%s.zip' % (self.base_url,self.application_id,series_id,language)
        print base_zip
        base_zip = self._get(base_zip)

        zip_stream = StringIO.StringIO()
        zip_stream.write(base_zip)
        base_zip = ZipFile(zip_stream)

        episodes = base_zip.open(language+'.xml').read()
        art = base_zip.open('banners.xml').read()
        meta_info = TVShow.from_xml(episodes,art)
        return meta_info

    def _get(self,url):
        retries = 5
        while retries > 0:
            try:
                response = urllib.urlopen(url)
                response = response.read()
                return response
            except IOError as e:
                print str(e)
                retries = retries-1


    def search(self,name,language='en'):
        GET_SERIES='GetSeries.php?seriesname='

        series_info = self._get(self.base_url+GET_SERIES+urllib.quote_plus(name)+'&language='+language)
        series_xml = etree.fromstring(series_info)
        series = series_xml.xpath('//Series')
        results = []
        for s in series:
            series_name = s.xpath('SeriesName')[0].text 
            overview = s.xpath('Overview')[0].text 
            series_id = int(s.xpath('seriesid')[0].text) 
            first_aired = s.xpath('FirstAired')[0].text 
            language = s.xpath('language')[0].text
            results.append((series_name,overview,first_aired,language,series_id))
        return results 
            

    def get_show_by_imdbid(self,imdbid):
        raise NotImplemented

    def get_show_by_zap2itid(self,zap2itid):
        raise NotImplemented

    def get_episode(self,series,air_date,language='en'):
        if isinstance(series,str):
            results = self.search(series,language)
            if len(results)==0:
                raise TVDBException("No series found for \"%s\"" % (series))
            elif len(results)>1: 
                raise TVDBException("Multiple series found for \"%s\"" % (series))
            series = results[0][4] 
        from datetime import date
        if not isinstance(air_date,date):
            raise TVDBException('air_date must be a datetime.date')

        info ='%sGetEpisodeByAirDate?apikey=%s&seriesid=%s&airdate=%s&language=%s' % (self.base_url,self.application_id,series,date.strftime(air_date,'%Y-%m-%d'),language)

        series_info = self._get(info)
        if '<Error>' in series_info:
            raise TVDBException('No episode found')
        import re
        return Episode.from_xml(re.search('.*(<Episode>.*</Episode>).*',series_info.replace('\n','')).groups()[0])
