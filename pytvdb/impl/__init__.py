from abc import ABCMeta


class TVDBShowProvider:
    __metaclass__ = ABCMeta

    def get_show(name,language='en'):
        raise NotImplemented

    

