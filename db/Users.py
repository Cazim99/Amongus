import sqlalchemy as sql
import sys,os

# GLOBAL MODULES
sys.path.append(os.path.abspath(os.path.join('..')))
from db import DBengine

class Users:

    @staticmethod
    def all(*fields):
        if len(fields) == 0:
            query = sql.text("SELECT * FROM Users;")
        else:
            query = sql.text(f"SELECT {','.join(*fields)} FROM Users;")
        connection = DBengine.connect()
        result = connection.execute(query).mappings().all()
        connection.close()
        return result

    @staticmethod
    def one(user_id : int, *fields):
        if len(fields) == 0:
            query = sql.text("SELECT * FROM Users WHERE ID = :ID;")
        else:
            query = sql.text(f"SELECT {','.join(*fields)} FROM Users WHERE ID = :ID;") 
        connection = DBengine.connect()
        result = connection.execute(query, { "ID": user_id }).mappings().first()
        connection.close()
        return result
    
    @staticmethod
    def by_username(username : int, *fields):
        if len(fields) == 0:
            query = sql.text("SELECT * FROM Users WHERE username = :username;")
        else:
            query = sql.text(f"SELECT {','.join(*fields)} FROM Users WHERE username = :username;") 
        connection = DBengine.connect()
        result = connection.execute(query, { "username": username }).mappings().first()
        connection.close()
        return result
    
    @staticmethod
    def by_email(email : str, *fields):
        if len(fields) == 0:
            query = sql.text("SELECT * FROM Users WHERE email = :email;")
        else:
            query = sql.text(f"SELECT {','.join(*fields)} FROM Users WHERE email = :email;") 
        
        connection = DBengine.connect()
        result = connection.execute(query, { "email": email }).mappings().first()
        connection.close()
        return result

    @staticmethod
    def create_user(user):
        error_message = None
        if Users.by_username(user['username']) != None:
             error_message = "User with that username already exists !"
             return error_message
        if Users.by_email(user['email']) != None:
             error_message = "User with that e-mail already exists !"
             return error_message

        user['health'] = 100
        user['movespeed'] = 3
        user['cordinates'] = '0,0' # Hospital door location in game
        user['baned'] = 0
        user['inside_ship'] = 0
        
        query = sql.text("""INSERT INTO Users (full_name, username, email, password, movespeed, health, cordinates, inside_ship, baned)
                                                values (:full_name, :username, :email, :password, :movespeed, :health, :cordinates,:inside_ship, :baned);""")
        connection = DBengine.connect()
        connection.execute(query, user)
        connection.commit()
        connection.close()
        return error_message


    @staticmethod
    def update_user_game_data(user):
        if Users.by_username(user['username']) != None:
            query = sql.text("""UPDATE Users SET cordinates=:cordinates, inside_ship=:inside_ship, baned=:baned, health=:health, movespeed=:movespeed WHERE username =:username;""") 
            connection = DBengine.connect()
            connection.execute(query, {"cordinates":f"{user['cordinates'][0]},{user['cordinates'][1]}",
                                       "health":user['health'],
                                       "movespeed":user['movespeed'],
                                       "username":user['username'],
                                       "inside_ship":1 if user['inside_ship'] else 0,
                                       "baned":1 if 'baned' in user else 0})
            connection.commit()
            connection.close()

    @staticmethod
    def update(user):
        error_message = None
        users = Users.all()
        
        if users != None:
            for u in users:
                if user['email'].strip() == u['email'] and user['username'] != u['username']:
                    error_message = "User with that e-mail already exists !"
                    return error_message
        
        query = sql.text("""UPDATE Users SET full_name = :full_name, username = :username, email = :email, password = :password WHERE username = :username;""") 
        connection = DBengine.connect()
        connection.execute(query, user)
        connection.commit()
        connection.close()
        return error_message

    @staticmethod
    def delete(user_id : int) -> int:
        query = sql.text("DELETE FROM Users WHERE ID = :ID;")
        connection = DBengine.connect()
        connection.execute(query, { "ID": user_id })
        connection.commit()
        connection.close()