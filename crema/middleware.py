import os
import logging
import subprocess, shlex, threading, time, signal
from subprocess import CalledProcessError
from django.conf import settings

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
        if response.status_code == 200:
            path = request.META['PATH_INFO']
            if path.endswith('.js'):
                print '[Crema] Brewing Coffeescript for: "%s"' % path
                self.brew(path)
        return response
    
    def fixPath(self, path):
        """docstring for fixPath"""
        rel_path = path.replace(self.brew_url, '')
        brewed_path = os.path.join(self.brewed, rel_path)
        unbrewed_path = os.path.join(self.unbrewed, rel_path.replace('.js', '.coffee'))
        return (brewed_path, unbrewed_path)
    
    def brew(self, path):
        """docstring for brew"""
        brewed_path, unbrewed_path = self.fixPath(path)
        
        if not os.path.exists(unbrewed_path):
            return
        
        cmd = '%s --output %s --compile %s' % (self.coffee, os.path.split(brewed_path)[0], unbrewed_path)
        
        print cmd
        
        subprocess.call(cmd, shell=True)