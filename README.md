# Amongus

potrebno je pripremiti bazu podataka

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

POTREBNO JE DA SU PORTOVI 9999,9998,9997 SLOBODNI, TAKO DA UKOLIKO NISU, IZMENITI (UGLAVNOM JESU NA SVAKOM RACUNARU)
Takodje podesiti konfiguracije za bazu podataka u config.ini fajlu a to se nalazi u GameServer folderu i folderu WebSite

NAKON TOGA 
   Pokrenuti main.py iz Web Site foldera 
   Pokrenuti GameServer.py iz GameServer foldera

Otvoriti web sajt na localhost:9997 i napraviti nalog

Pokrenuti igricu iz folder Amongus main.py 

Uzivajte !
