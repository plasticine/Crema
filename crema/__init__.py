VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))



DEFAULT_COFFEESCRIPT_CMD = '/usr/local/bin/coffee'


class Crema(object):
    """
    
    """
    
    def __init__(self, coffee, source, dest, watch=True):
        super(Crema, self).__init__()
        self.coffee = coffee if coffee else DEFAULT_COFFEESCRIPT_CMD
        self.source = source
        self.dest = dest
        self.watch = watch
        