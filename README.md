# AMONGUS
It is necessary to prepare a database

  ||
  ||
  \/

  --------------------------------------------------------
  --------------------------------------------------------

    CREATE DATABASE IF NOT EXISTS zimca_games;

    use zimca_games;

    CREATE TABLE `users` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `full_name` varchar(255) NOT NULL,
      `username` varchar(255) NOT NULL,
      `email` varchar(255) NOT NULL,
      `password` varchar(255) NOT NULL,
      `movespeed` int NOT NULL,
      `health` int NOT NULL,
      `inside_ship` bool NOT NULL,
      `cordinates` varchar(255) NOT NULL,
      PRIMARY KEY (`ID`)
    )

  --------------------------------------------------------
  --------------------------------------------------------

PORTS 9999,9998,9997 ARE FREE, SO IF THEY ARE NOT, CHANGE (MOSTLY ON EVERY COMPUTER)
Also set configurations for the database in config.ini file and this is located in the GameServer folder and the WebSite folder

AFTER THAT 
   Run main.py from Web Site folder 
   Run GameServer.py from GameServer folder

Open a website at localhost:9997 and create an account

Run the game from the Folder Amongus-Game -> main.py 

Enjoy!
