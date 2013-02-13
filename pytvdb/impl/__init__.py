from abc import ABCMeta


class TVDBShowProvider:
    __metaclass__ = ABCMeta

    def get_show(name,language='en'):
        raise NotImplemented

    def search(name,language='en'):
        raise NotImplemented
    
    def get_show_by_imdbid(imdbid):
        raise NotImplemented
    
    def get_show_by_zap2itid(zap2itid):
        raise NotImplemented
    
    def get_episode(series,air_date,language='en'):
        raise NotImplemented

