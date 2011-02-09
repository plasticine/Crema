import os
import logging
from django.conf import settings
from crema import Crema

logger = logging.getLogger(__name__)

CONTENT_TYPES_TO_BREW = ('text/html', 'application/xhtml+xml')


class CremaMiddleware(object):
    """
    Middleware to find any coffeescripts & brew them up!
    
      \ | ( | ) / /
    _________________
    |               |
    |               |
    |               /--\
    |               |  |
     \             /\--/
      \___________/
    
    """
    
    def __init__(self):
        if hasattr(settings, 'CREMA_CONFIG'):
            command = settings.CREMA_CONFIG.get('COFFEESCRIPT_CMD', None)
            coffeescript_source = settings.CREMA_CONFIG.get('COFFEESCRIPT_DIR', None)
            brew_dest = settings.CREMA_CONFIG.get('BREW_DIR', None)
            
            self.crema = Crema(coffee=command, source=coffeescript_source, destination=brew_dest)
    
    def process_response(self, request, response):
        """
        
        """
        
        raise False
        
        if response.status_code == 200:
            if response['Content-Type'].split(';')[0] in CONTENT_TYPES_TO_BREW:
                self.crema.extract()