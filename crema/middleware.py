import os
import logging
import subprocess, shlex, threading, time, signal
from subprocess import CalledProcessError
from django.conf import settings
from django.http import HttpResponse

logger = logging.getLogger(__name__)

CONTENT_TYPES_TO_BREW = ('text/html', 'application/xhtml+xml')
DEFAULT_COFFEESCRIPT_CMD = '/usr/local/bin/coffee'


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
            self.coffee = settings.CREMA_CONFIG.get('COFFEESCRIPT_CMD', DEFAULT_COFFEESCRIPT_CMD)
            self.unbrewed = settings.CREMA_CONFIG.get('COFFEESCRIPT_DIR', None)
            self.brewed = settings.CREMA_CONFIG.get('BREW_DIR', None)
            self.brew_url = settings.CREMA_CONFIG.get('BREW_URL', os.path.join(settings.MEDIA_URL, 'scripts/'))
            
            if not self.brew_url.endswith('/'):
                self.brew_url = self.brew_url+'/'
    
    def process_response(self, request, response):
        """
        
        """
        if response['Content-Type'].split(';')[0] in CONTENT_TYPES_TO_BREW:
            path = request.META['PATH_INFO']
            for directory, dirnames, filenames in os.walk(self.unbrewed):
                for file in filenames:
                    if file.endswith('.coffee'):
                        # print '[Crema] Brewing Coffeescript for: "%s"' % os.path.join(directory, file)
                        brew = self.brew(os.path.join(directory, file))
                        if brew is not 0:
                            return HttpResponse('<pre>%s</pre>' % (brew))
        return response
    
    def fix_path(self, path):
        """
        
        """
        rel_path = path.replace(self.unbrewed, '')
        brewed_path = os.path.join(self.brewed, rel_path[1:])
        unbrewed_path = os.path.join(self.unbrewed, rel_path[1:])
        return (brewed_path, unbrewed_path)
    
    def brew(self, path):
        """
        
        """
        brewed_path, unbrewed_path = self.fix_path(path)
        cmd = '%s --output %s --compile %s' % (self.coffee, os.path.split(brewed_path)[0], unbrewed_path)
        process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = process.communicate()
        
        if process.returncode is 1:
            return out[1]
        return 0