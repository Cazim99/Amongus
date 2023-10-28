import sqlalchemy


class DBengine:
    DB_CONFIG = None
    CHARSET_FORMAT = "?charset=utf8"
    ENGINE = None
    
    @staticmethod
    def create_engine():
        url = DBengine.DB_CONFIG["db_protocol"] + "+" + DBengine.DB_CONFIG["db_lib"] + "://"
        if "user" in DBengine.DB_CONFIG.keys():
            url += DBengine.DB_CONFIG["user"]
            if "password" in DBengine.DB_CONFIG.keys():
                url += ":" + DBengine.DB_CONFIG["password"]
            url += "@"
        url += DBengine.DB_CONFIG["host"]
        if "port" in DBengine.DB_CONFIG.keys():
            url += ":" + str(DBengine.DB_CONFIG["port"])
        url += "/" + DBengine.DB_CONFIG["db_name"] + DBengine.CHARSET_FORMAT
        
        return sqlalchemy.create_engine(url, echo=DBengine.DB_CONFIG["echo"])
            
    
    @staticmethod
    def connect() -> sqlalchemy.Connection:
        if DBengine.ENGINE is None:
            DBengine.ENGINE = DBengine.create_engine()
        return DBengine.ENGINE.connect()