from klase.Game import Game
from ConfigLoader import ConfigLoader
from klase.LAUNCHER_GUI.LauncherWindow import LauncherWindow
import pymsgbox

config_file_informations = {
    "settings":
        {
            'items':{
                'full_screen':'bool',
                'first_time_run':'bool',
                'sound_on':'bool',
                'dev_mode':'bool',
                'screen_size':'other',
                'game_server_host':'str',
                'game_server_port':'int',
                'website_host':'str',
                'website_port':'int',
            }
        },
}
CONFIGURATIONS = ConfigLoader.Load("config.ini", config_file_informations) # Load all configurations
GAME_CONFIGURATIONS = CONFIGURATIONS['settings']['items'] # Load settings section from configuratios for game

GMSERVER = (GAME_CONFIGURATIONS['game_server_host'], # HOST
            GAME_CONFIGURATIONS['game_server_port']) # PORT
GMWEBSITE = (GAME_CONFIGURATIONS['website_host'],
             GAME_CONFIGURATIONS['website_port']) # HOST, PORT

launcher = LauncherWindow(website=GMWEBSITE)
launcher.mainloop()
launcher.quit()

if launcher.user != None:
    AmongUs = Game(gamename="Amongus",  # GAME NAME
                    screen_size=GAME_CONFIGURATIONS['screen_size'], # GAME SCREEN SIZE
                    full_screen=GAME_CONFIGURATIONS['full_screen'], # GAME FULL SCREEN OR NOT
                    dev_mode=GAME_CONFIGURATIONS['dev_mode'],# GAME DEVELOPMENT MODE OR NOT
                    server=GMSERVER, # GAME SERVER (HOST,PORT)
                    soundOn=GAME_CONFIGURATIONS['sound_on'],
                    user=launcher.user,
                    first_time_run=GAME_CONFIGURATIONS['first_time_run'],
                    )
    AmongUs.start() # START GAME
    while True:
        if AmongUs.restart is not None:
            AmongUs = Game(gamename="Amongus",  # GAME NAME
                screen_size=GAME_CONFIGURATIONS['screen_size'], # GAME SCREEN SIZE
                full_screen=AmongUs.restart['fullscreen'],
                dev_mode=GAME_CONFIGURATIONS['dev_mode'],# GAME DEVELOPMENT MODE OR NOT
                server=GMSERVER, # GAME SERVER (HOST,PORT)
                user=launcher.user,
                soundOn=AmongUs.restart['soundOn'],
                first_time_run=GAME_CONFIGURATIONS['first_time_run'],
                )
            AmongUs.start() # START GAME
        else:
            break

    if AmongUs.exit_message is not None:
        pymsgbox.alert(AmongUs.exit_message, 'Amongus')