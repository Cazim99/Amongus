"""
THIS MODULE IS CREATE BY CAZIM HAMIDOVIC (ZC-Team)
CONTACT INFO: cazimhamidovic@outlook.com


HOW TO USE EXAMPLE ( bool, str, int and other means what type is item value in .ini file)

config_file_informations = {
    "settings": # SECTION NAME
        {
            'items':{ # SECTION ITEMS 
                'full_screen':'bool',
                'dev_mode':'bool',
                'screen_size':'other',
                'server_host':'str',
                'server_port':'int',
            }
        },
}

CONFIGURATIONS = ConfigLoader.Load("config.ini", config_file_informations)

"""
import configparser
import os
import ast

class FileCantBeFound(Exception):
    def __init__(self,config_file_path):
        super().__init__(f"File '{config_file_path}' cant be found.")
        
class NoSectionInConfigFile(Exception):
    def __init__(self, section):
        super().__init__(f"[ConfigLoader][ERROR] Section '{section}' not found in file...") 
        
class NoIteminSection(Exception):
    def __init__(self, item, section):
        super().__init__(f"[ConfigLoader][ERROR] Cant find item '{item}' in section '{section}' ") 

class ConfigLoader:
    
    @staticmethod
    def Load(config_file_path:str, config_file_informations:dict) -> dict:
        if not os.path.exists(config_file_path):
            raise FileCantBeFound(config_file_path)
        else:
            print("[ConfigLoader][INFO] reading config file...")
        try:
            config = configparser.ConfigParser()
            config.read(config_file_path)
            print("[ConfigLoader][INFO] config file loaded !")
        except:
            print("[ConfigLoader][ERROR] unknow problem with reading config file...")
         
        
        print("[ConfigLoader][INFO] Loading sections...")
        SECTIONS = []
        for section in config_file_informations.keys():
            if section in config._sections:
                SECTIONS.append(section)
            else:
                raise NoSectionInConfigFile(section) 
        print(f"[ConfigLoader][INFO] loaded sections: {SECTIONS}!")
        
        print("[ConfigLoader][INFO] Loading items from sections...")
        ITEMS = []
        for section in SECTIONS:
            for item in config._sections[section]:
                ITEMS.append(item)
        
        
        for section in SECTIONS:
            for item in config_file_informations[section]['items'].keys():
                if item in ITEMS:
                    if config_file_informations[section]['items'][item] == 'str':  
                        config_file_informations[section]['items'][item] = str(config._sections[section][ITEMS[ITEMS.index(item)]])
                    elif config_file_informations[section]['items'][item] == 'int':
                        config_file_informations[section]['items'][item] = int(config._sections[section][ITEMS[ITEMS.index(item)]])
                    elif config_file_informations[section]['items'][item] == 'bool':
                        if config._sections[section][ITEMS[ITEMS.index(item)]] == 'False':
                            config_file_informations[section]['items'][item] = False
                        else:
                            config_file_informations[section]['items'][item] = True
                    else:
                        config_file_informations[section]['items'][item] = ast.literal_eval(config._sections[section][ITEMS[ITEMS.index(item)]])
                else:
                    raise NoIteminSection(item,section) 
                
        print(f"[ConfigLoader][INFO] loaded items")
        config_file = config_file_informations
        return config_file

