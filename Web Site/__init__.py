import os, sys
from ConfigLoader import ConfigLoader

config_file_informations = {
    "server":
        {
            'items':{
                'host':'str',
                'port':'int',
                'debug':'bool',
                'game_download_link':'str',
            }
        },
    "database":
        {
            'items':{
                'db_protocol':'str',
                'db_lib':'str',
                'db_name':'str',
                'user':'str',
                'host':'str',
                'port':'int',
                'echo': 'bool',
            }
        }
}
CONFIGURATIONS = ConfigLoader.Load("config.ini", config_file_informations)

PATCH_LIST = [{'version':'1.4',"type":'Now you can chat with friends inside the game'},
              {'version':"1.3","type":"Fixed bug with images scalling"},
              {'version':"1.2","type":"Now you can play with friends, its online !"},
              {'version':"1.1","type":"Created basics of game"},
              {'version':"1.0","type":"Created website"},]

inputs_rules = {
                'full_name': 
                    {
                        'name':"Full name",
                        'min-len':3,
                        'max-len':30,
                        'same-check':None,
                    },
                'username':
                    {
                        'name':"Username",
                        'min-len':3,
                        'max-len':None,
                        'same-check':None,
                    },
                'email':
                    {
                        'name':"E-mail",
                        'min-len':3,
                        'max-len':None,
                        'same-check':None,
                    },
                'password': 
                    {
                        'name':"Password",
                        'min-len':8,
                        'max-len':None,
                        'same-check':'confirm-password',
                    },
                'confirm-password':
                    {
                        'name':"Confirm password",
                        'min-len':8,
                        'max-len':None,
                        'same-check':'password',
                    },
                }

inputs_rules_update = {
                'full_name': 
                    {
                        'name':"Full name",
                        'min-len':3,
                        'max-len':30,
                        'same-check':None,
                    },
                'username':
                    {
                        'name':"Username",
                        'min-len':3,
                        'max-len':None,
                        'same-check':None,
                    },
                'email':
                    {
                        'name':"E-mail",
                        'min-len':3,
                        'max-len':None,
                        'same-check':None,
                    },
                'password': 
                    {
                        'name':"Password",
                        'min-len':8,
                        'max-len':None,
                        'same-check':None,
                    }
                }