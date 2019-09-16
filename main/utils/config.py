# -*- coding: utf-8 -*-

import ConfigParser
import os
import sys

class config_manager(object):

    def __init__(self, filename=None):
        self.rcfile = filename
        self.options = {}
        self.misc = {}
        self.parse_config()

    def __getitem__(self, key):
        return self.options[key]

    def load(self):
        parser = ConfigParser.ConfigParser()
        try:
            parser.read([self.rcfile])
            
            for sec in parser.sections():
                if sec == 'options':
                    for name, value in parser.items('options'):
                        if value.upper() == 'TRUE':
                            value = True
                        elif value.upper() == 'FALSE':
                            value = False
                        self.options[name] = value
                else:
                    for name, value in parser.items(sec):
                        if value.upper() == 'TRUE':
                            value = True
                        elif value.upper() == 'FALSE':
                            value = False
                        if not self.misc.has_key(sec):
                            self.misc[sec] = {}
                        self.misc[sec][name] = value
        except IOError, ConfigParser.NoSectionError:
            pass
    def save(self):
        # if configfile is not exists, create it 
        try:
            config_exists = os.path.exists(self.rcfile)
            if not config_exists: 
                if not os.path.exists(os.path.dirname(self.rcfile)):
                    os.makedirs(os.path.dirname(self.rcfile))
                parser = ConfigParser.ConfigParser()
                parser.add_section('options')
                for option in sorted(self.options.keys()):
                    parser.set('options', option, self.options[option])

                for sec in sorted(self.misc.keys()):
                    parser.add_section(sec)
                    for opt in sorted(self.misc[sec].keys()):
                        parser.set(sec, opt, self.misc[sec][opt])
                # write config file
                try:
                    parser.write(file(self.rcfile, 'w'))
                    if not config_exists:
                        os.chmod(self.rcfile, 0600)
                except IOError:
                    sys.stderr.write("ERROR: couldn't write the config file\n")
        except OSError:
            sys.stderr.write("ERROR: couldn't write the config file\n")

    def parse_config(self):
        if os.name == 'nt':
            config_file_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'wechat_server.conf')
        else:
            config_file_path = os.path.expanduser('~/.wechat_server')
        self.rcfile = os.path.abspath(config_file_path)
        self.load()
        self.save()
    
    def get(self, key, default=None):
        return self.options.get(key, default)

    def get_misc(self, sect, key, default=None):
        return self.misc.get(sect,{}).get(key, default)
config = config_manager()
