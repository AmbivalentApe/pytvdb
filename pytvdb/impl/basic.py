from zipfile import ZipFile
import StringIO
from lxml import etree
import urllib
from ..model.tv_show import TVShow
from ..model.episode import Episode
from ..model.exceptions import TVDBException
from . import TVDBShowProvider
import logging
import os
import re
from datetime import date

class HttpTVDBAdapter(TVDBShowProvider):
    '''
    Simple non caching implementation of the TVDB.com public api.
    
    '''

    def __init__(self,application_id=None,base_url='http://www.thetvdb.com/api/',):
        '''
        Constructor. 

        'application_id' should be the unique id registered to your application.
        If application_id is None then TVDBAPPLICATIONID needs to be set as an env variable
        
        '''
        self.logger = logging.getLogger('httptvdbadapter')
        if application_id is None:
            if 'TVDBAPPLICATIONID' not in os.environ:
                raise TVDBException(message='application_id is None and TVDBAPPLICATIONID is not set')
            self.application_id = os.environ['TVDBAPPLICATIONID']
        else:
            self.application_id = application_id
        self.base_url = base_url
        
    def get_show(self,name,language='en'):
        """
        Returns a TVShow instance representing the show searched for (unpacked fully).

        Searching comprises a two step process:

        1) Locate the unique ID for the series
        2) Pull the XML payloads for the series and unpack into objects (payload is a ZIP file comprising 1* XML for series,episodes and art) 

        """
        
        GET_SERIES='GetSeries.php?seriesname='
        series_info = self._get(self.base_url+GET_SERIES+urllib.quote_plus(name)+'&language='+language)
        self.logger.debug('Fetching series info for \"%s\" language=(%s)' % (name,language))
        series_xml = etree.fromstring(series_info)


        # we get back an xml document that contains no series info if there isn't a match
        series_id = series_xml.xpath('//seriesid')
        if len(series_id)==0:
            raise TVDBException("No series found for \"%s\"" % (name))
        # equally, error if more than one comes back

        elif len(series_id)>1: 
            raise TVDBException("Multiple series found for \"%s\"" % (name))
        series_id = series_id[0].text

        self.logger.debug('Series set to %s' % (series_id))
        base_zip = '%s%s/series/%s/all/%s.zip' % (self.base_url,self.application_id,series_id,language)
        self.logger.debug('Fetching zip file')
        base_zip = self._get(base_zip)

        zip_stream = StringIO.StringIO()
        zip_stream.write(base_zip)
        base_zip = ZipFile(zip_stream)

        episodes = base_zip.open(language+'.xml').read()
        art = base_zip.open('banners.xml').read()
        meta_info = TVShow.from_xml(episodes,art)
        return meta_info

    def _get(self,url):
        """
        Internal search method. Given tvdb.com sometimes struggles under load,
        maintain internal state and retry for 5 times before giving up.
        """
        retries = 5
        last_exception = None
        while retries > 0:
            try:
                self.logger.debug('Fetching %s',url)
                response = urllib.urlopen(url)
                response = response.read()
                return response
            except IOError as e:
                logger.exception(e)
                retries = retries-1
                last_exception = e # track this so we can rethrow it
        raise TVDBException(last_exception)


    def search(self,name,language='en'):
        '''
        Search for series matching the name and (optional) language.

        Returns a quintuple of (Series Name, Overview, seriesID, First Aired Date and language)
        '''
        GET_SERIES='GetSeries.php?seriesname='
        self.logger.debug('Searching for \"%s\" language=(%s)' % (name,language))

        series_info = self._get(self.base_url+GET_SERIES+urllib.quote_plus(name)+'&language='+language)
        series_xml = etree.fromstring(series_info)
        series = series_xml.xpath('//Series')
        self.logger.debug('Found %s results' % (len(series)))
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
        '''
        Return an Episode instance for a given series and air date combination.
       
        If 'series' is a string, it is assumed to be a name and series id is looked up.
        If 'series' is an int, it is assumed to be the TVDB series id

        '''
        if isinstance(series,str):
            results = self.search(series,language)
            if len(results)==0:
                raise TVDBException("No series found for \"%s\"" % (series))
            elif len(results)>1: 
                raise TVDBException("Multiple series found for \"%s\"" % (series))
            series = results[0][4]
        elif not isinstance(series,int):
            raise TVDBException('series must either be str or int')
        if not isinstance(air_date,date):
            raise TVDBException('air_date must be a datetime.date')

        info ='%sGetEpisodeByAirDate?apikey=%s&seriesid=%s&airdate=%s&language=%s' % (self.base_url,self.application_id,series,date.strftime(air_date,'%Y-%m-%d'),language)

        series_info = self._get(info)
        if '<Error>' in series_info:
            raise TVDBException('No episode found')
        return Episode.from_xml(re.search('.*(<Episode>.*</Episode>).*',series_info.replace('\n','')).groups()[0])
