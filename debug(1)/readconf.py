# -*- coding:utf-8 -*-
import configparser
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

# config_init = configparser.ConfigParser()
# path = os.path.split(os.path.realpath(__file__))[0]
# print('##### 配置文件读取目录为：' + path + "\\b.conf")
# config_init.read(os.path.join(path, 'config/config.ini'), encoding='utf-8-sig')



class OperationalError(Exception):
    """operation error."""
class Dictionary(dict):
    """ custom dict."""
    def __getattr__(self, key):
        return self.get(key, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Config:
    def __init__(self, file_name="b", cfg=None):
        """
        @param file_name: file name without extension.
        @param cfg: configuration file path.
        """
        env = {}
        for key, value in os.environ.items():
            if key.startswith("TEST_"):
                env[key] = value

        config = configparser.ConfigParser(env)

        if cfg:
            config.read(cfg)
        else:
            config.read(os.path.join(current_dir, "conf", "%s.conf" % file_name))

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_value in config.items(section):
                try:
                    # Ugly fix to avoid '0' and '1' to be parsed as a
                    # boolean value.
                    # We raise an exception to goto fail^w parse it
                    # as integer.
                    if config.get(section, name) in ["0", "1"]:
                        raise ValueError

                    value = config.getboolean(section, name)
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)

                setattr(getattr(self, section), name, value)

    def get(self, section):
        """Get option.
        @param section: section to fetch.
        @return: option value.
        """
        try:
            return getattr(self, section)
        except AttributeError as e:
            raise OperationalError("Option %s is not found in "
                                   "configuration, error: %s" %
                                   (section, e))






