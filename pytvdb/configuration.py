import os
import ConfigParser

__CONFIGFILE__ = '.pytvdb'
__ROOTSECTION__ = 'PYTVDB'
__IMPLEMENTATION__ = 'implementation'

def setup():
    global __CONFIGFILE__, __ROOTSECTION__,__IMPLEMENTATION__
    app_id = raw_input("TVDB.com application ID:")
    implementation = raw_input('Implementation (press return to default)')
    args = {}
    if implementation =='':
        implementation = 'pytvdb.impl.basic.HttpTVDBAdapter'
        args = {'application_id':app_id}
    components = implementation.split('.')
    item = simple_loader(implementation)
    import ConfigParser
    config = ConfigParser.SafeConfigParser()
    config.add_section(__ROOTSECTION__)
    config.set(__ROOTSECTION__,__IMPLEMENTATION__,implementation)
    config.add_section(implementation)
    for (K,V) in args.items():
        config.set(implementation,K,V)

    with open(os.path.join(os.environ['HOME'],__CONFIGFILE__),'w') as configfile:
        config.write(configfile)
    return item(**args)

def simple_loader(class_name):
    components = class_name.split('.')
    item = __import__('.'.join(components[0:-1]))
    for module in components[1:]:
        item = getattr(item,module)
    return item

def bootstrap(configparser = None):
    '''
    internal bootstrap function 
   
    Attempt to find a .pytvdb file and configure based on that, else return _setup
    '''
    global __CONFIGFILE__, __ROOTSECTION__,__IMPLEMENTATION__
    if configparser is None:
        configparser = ConfigParser.SafeConfigParser()
        results = configparser.read([os.path.join(os.getcwd(),__CONFIGFILE__),os.path.join(os.environ['HOME'],__CONFIGFILE__)])
        if len(results)==0:
            return setup()
    from pytvdb.model.exceptions import TVDBException
    if configparser.has_section(__ROOTSECTION__):
        if configparser.has_option(__ROOTSECTION__,__IMPLEMENTATION__):
            implementation = configparser.get(__ROOTSECTION__,__IMPLEMENTATION__).rstrip()
            item = simple_loader(implementation)
            args = {}
            if configparser.has_section(implementation):
                args = {X:configparser.get(implementation,X) for X in configparser.options(implementation)}
                return item(**args)
        else:
            raise TVDBException('No %s specified in %s section' % (__IMPLEMENTATION__,__ROOTSECTION__))
    else:
        raise TVDBException('No %s section in %s file' % (__ROOTSECTION__,__CONFIGFILE__))
