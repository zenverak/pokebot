import sqlite3
from datetime import datetime
import logging


import globals

dbConn = None


def init():
    global dbConn
    dbConn = sqlite3.connect(globals.database_name)
    c = dbConn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS pokemon(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    trainer char(20),
                    name char(20),
                    species char(20),
                    hp int,
                    atk int,
                    def int,
                    spatk int,
                    spdef int,
                    speed int,
                    atk1 char(200),
                    atk2 char(200),
                    atk3 char(200),
                    atk4 char(200),
                    about char(1000)
              )''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS battle_pokemon(
                    trainer char(20),
                    name char(20),
                    species char(20),
                    hp int,
                    atk int,
                    def int,
                    spatk int,
                    spdef int,
                    speed int,
                    atk1 char(200),
                    atk2 char(200),
                    atk3 char(200),
                    atk4 char(200),
                    about char(1000)
              )''')


    c.execute('''
            CREATE TABLE IF NOT EXISTS trainer(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    trainer char(20),
                    role char(25)
              )''')
            
            
    c.execute('''
            CREATE TABLE IF NOT EXISTS inbattle(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    trainer char(20),
                    room char(30)
              )''')

    dbConn.commit()
            

            
init()


def create_pokemon(trainer, name, species, hp, atk, _def, spatk, spdef, speed, atk1, atk2, atk3, atk4, story):
    c = dbConn.cursor()
    statement = '''insert into pokemon(trainer,name, species, hp, atk, def, spatk, spdef, speed, atk1, atk2, atk3, atk4, about) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    print (statement)
    try:
        c.execute(statement,(trainer.lstrip(' '), name.lstrip(' '), species.lstrip(' '), hp, atk, _def, spatk, spdef, speed, atk1.lstrip(' '), atk2.lstrip(' '), atk3.lstrip(' '), atk4.lstrip(' '), story.lstrip(' '),))
        dbConn.commit()
        return True, ''
    except Exception as e:
        print("Failed to create pokemon")
        print(e)
        return False, e

def get_pokemon(trainer,name):
    c = dbConn.cursor()
    print("Trainer is {} and name is {}".format(trainer, name))
    statement =  '''select * from pokemon where trainer=? and lower(name)=?'''
    try:
        c.execute(statement,(trainer,name.lower(),))
        pokemon = c.fetchall()
        print(pokemon)
        return pokemon,''
    except Exception as e:
        print("Failed to get pokemon")
        print(e)
        return False,e


def get_battle_pokemon(trainer,name):
    c = dbConn.cursor()
    statement =  '''select * from battle_pokemon where trainer=? and lower(name)=?'''
    try:
        c.execute(statement,(trainer,name.lower(),))
        pokemon = c.fetchall()
        return pokemon, ''
    except Exception as e:
        print("Failed to get pokemon")
        print(e)
        return False, e

def get_all_pokemon(trainer):
    c = dbConn.cursor()
    try:
        c.execute('''select * from pokemon where trainer=?''',(trainer,))
        return c.fetchall()
    except:
        print("Failed to get ticket")
        return False

def start_battle(trainer, room):
    c = dbConn.cursor()
    statement = '''insert into inbattle(trainer, room) values(?,?)'''
    print('got cursor')
    try:
        c.execute(statement,(trainer, room,))
        dbConn.commit()
        return True, ''
    except Exception as e:
        print("failed to start battle")
        return False, e

def end_battle(trainer):
    c = dbConn.cursor()
    try:
        c.execute('''delete from inbattle where trainer=?''',(trainer, ))
        c.execute('''delete from battle_pokemon where trainer=?''',(trainer,))
        dbConn.commit()
        return True, ''
    except Exception as e:
        print("failed to end battle")
        return False, e

def room_in_use(room):
    c = dbConn.cursor()
    statement = '''select * from inbattle where room=?'''
    print(room)
    try:
        c.execute(statement,(room,))
        return c.fetchall(),''
    except Exception as e:
        print("Failed to check if room was in use")
        return False, e
        
def trainer_in_battle(trainer):
    c = dbConn.cursor()
    statement = '''select * from inbattle where trainer=?'''
    try:
        c.execute(statement,(trainer,))
        return c.fetchall()
    except:
        print("failed to check if trainer was in a room")
        return False
        
def right_room(trainer, room):
    c = dbConn.cursor()
    statement = '''select * from inbattle where trainer=? and room=?'''
    try:
        c.execute(statement, (trainer,room))
        return c.fetchall(),''
    except Exception as e:
        return False, e


def choose_pokemon(trainer, name):
    c = dbConn.cursor()
    try:
        c.execute('''insert into battle_pokemon  select trainer, name, species, hp, atk, def, spatk, spdef, speed, atk1, atk2, atk3, atk4, about  from pokemon where trainer=? and lower(name)=?''',(trainer, name.lower()))
        dbConn.commit()
        return True,''
    except Exception as e:
        print("failed to choose pokemon")
        return False , e


def update_stat(trainer, name, stat, value, battle=False):
    c = dbConn.cursor()
    table = 'pokemon'
    if battle:
        table = 'battle_pokemon'
    try:
        c.execute('''update {} set {} = ? where trainer=? and name=?  '''.format(table, stat),(value, trainer, name,))
        dbConn.commit()
        return True,''
    except Exception as e:
        print ("It has failed to update stat on table {}".format(table))
        return False,e
        

def delete_pk(trainer, name):
    c = dbConn.cursor()
    statement = '''delete from pokemon where trainer=? and lower(name)=?'''
    try:
        c.execute(statement,(trainer,name.lower()))
        dbConn.commit()
        return True,''
    except Exception as e:
        return False, e


def list_pk(trainer):
    c = dbConn.cursor()
    statement = '''select name, species from pokemon where trainer=? '''
    try:
        c.execute(statement, (trainer,))
        return c.fetchall(),''
    except Exception as e:
        return False, e
    
    

