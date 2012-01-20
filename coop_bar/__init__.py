# -*- coding: utf-8 -*-

VERSION = (0, 3, 2)

def get_version():
    return '%s.%s.%s' % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()

from django.utils.importlib import import_module
from django.conf import settings

class CoopBar:
    __we_are_all_one = {}
    
    def __init__(self):
        self.__dict__ = self.__we_are_all_one #Borg pattern
        
        if not self.__dict__: #Don't reload for each instance
            self._callbacks = []
            self._headers = []
            
            if hasattr(settings, 'COOPBAR_MODULES'):
                for module_name in settings.COOPBAR_MODULES:
                    try:
                        app_admin_bar_module = import_module(module_name)
                        loader_fct = getattr(app_admin_bar_module, 'load_commands')
                        loader_fct(self)
                    except ImportError:
                        raise ImportError(u"coop_bar : error while loading '{0}'. Check COOPBAR_MODULES in settings".format(module_name)) 
            else:
                for app in settings.INSTALLED_APPS:
                    try:
                        #load dynamically the admin_bar module of all apps
                        app_admin_bar_module = import_module(app+'.coop_bar_cfg')
                        if hasattr(app_admin_bar_module, 'load_commands'):
                            #call the load_commands function in this module
                            #This function should call the AdminBar:register_command for
                            #every item it want to insert in the bar
                            loader_fct = getattr(app_admin_bar_module, 'load_commands')
                            loader_fct(self)
                    except ImportError:
                        pass
        
    def register_header(self, callback):
        self._headers.append(callback)
        
    def register_command(self, callback):
        self._callbacks.append(callback)
        
    def register_separator(self):
        self._callbacks.append(None)
                
    def get_commands(self, request, context):
        commands = []
        separator = '<div class="separator"></div>'
        for c in self._callbacks:
            if c == None:
                #Replace None by separator. Avoid 2 following separators
                if commands and commands[-1]!=separator:
                    html = separator
                else:
                    html = ''
            else:
                #when a page wants to display the admin_bar
                #calls the registred callback in order to know what to display
                html = c(request, context)
            if html:
                commands.append(html)
        if commands and commands[-1]==separator:
            commands = commands[:-1]
        return commands
    
    def get_headers(self, request, context):
        headers = []
        for c in self._headers:
            html = c(request, context)
            if html:
                headers.append(html)
        return headers
