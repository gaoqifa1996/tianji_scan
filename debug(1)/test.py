import configparser
import os

config_init = configparser.ConfigParser()
path = os.path.split(os.path.realpath(__file__))[0]
print('#### 配置文件读取目录为：' + path + " ####")
config_init.read(os.path.join(path, 'config/config.ini'), encoding='utf-8-sig')

print(config_init.sections())

print()