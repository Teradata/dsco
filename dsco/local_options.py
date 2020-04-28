"""Read configuration optinos from $HOME/.dsco
"""
from pathlib import Path
import json

config_home = Path.home() / ".dsco"


class Settings(object):
    """Read settings from settings_file

    Methods
        get_local_settings (Dict):
            Static method that returns settings_file as dict

        get_local_kernal (Dict):
            Static method that returns localhost kernal

        get_remote_kernal_list (List[Dict]): 
            Static method that returns the remote 
            machines listed in settigns_file
    """
    settings_file = config_home / "settings.json"

    @classmethod
    def get_local_settings(cls):
        """Get local configuration options

        Retrieves the settings, if any, from settings_file
        """
        if cls.settings_file.exists():
            settings = json.load(cls.settings_file.open())
        else:
            settings = dict(loaded=True)
        
        return settings

    @classmethod
    def get_local_kernal(cls, settings={}):
        # mutate settings
        if not settings:
            settings.update(cls.get_local_settings())

        # Default values for local_kernal
        local_kernal = dict(name="localhost", properties=dict(ip="localhost"), env={})
        # Override with anything found in settings["local"]
        local_kernal.update(settings.get("local", {}))

        return local_kernal
        
    @classmethod
    def get_remote_kernal_list(cls, settings={}):
        """Get configuration information on remote machines

        Retrieves the list of remote machines from 
        $HOME/.dsco/settings.json. Each item in the list is expected
        to include:

            - name (str)
            - ip (str)
            - env (dict)
        """
        # mutate settings
        if not settings:
            settings.update(cls.get_local_settings())
        
        remote_list = settings.get("remote", [])

        return remote_list