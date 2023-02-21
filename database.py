""" database.py """
import json
from jsonpath import jsonpath
from mongoengine import connect
import os
import urllib.parse

from models import Enemy, Level, Game, Powerup


MG_HOST_DB = os.getenv('GRAPHENE_MG_DB_HOST', default='')
MG_PORT_DB = int(os.getenv('GRAPHENE_MG_DB_PORT', default='0'))
MG_USER_DB = os.getenv('GRAPHENE_MG_DB_USER', default='')
MG_PASSWORD_DB = os.getenv('GRAPHENE_MG_DB_PASS', default='')
MG_DATABASE_NAME = os.getenv('GRAPHENE_MG_DB_NAME', default='')

client = connect(
    MG_DATABASE_NAME,
    host = f'mongodb://{MG_USER_DB}:{(urllib.parse.quote_plus(MG_PASSWORD_DB, safe="/")).replace("/","%5C")}@{MG_HOST_DB}:{MG_PORT_DB}',
    alias="default",
)
client.drop_database(MG_DATABASE_NAME)


def init_db():

    with open("smb.json", "r") as file:
        data = json.loads(file.read())
    game = Game(name=data[0].get("table_data").get("Game"))
    game.save()

    for row in data:
        enemies = []
        for elem in row["enemies"]:
            amount = elem["amount"] if isinstance(elem["amount"], int) else 1
            enemy = Enemy(name=elem["name"], amount=amount)
            enemy.save()
            enemies.append(enemy)

        powerups = []
        for elem in row["statistics"]:
            powerup = Powerup(name=elem["name"], amount=elem["amount"])
            powerup.save()
            powerups.append(powerup)

        level = Level(
            description=row.get("description"),
            name=jsonpath(row, "table_data.World-Level")[0],
            world=jsonpath(row, "table_data.World")[0],
            time_limit=jsonpath(row, "table_data.Time limit")[0].split(" ")[0],
            boss=row.get("table_data").get("Boss"),
            enemies=enemies,
            game=game,
            powerups=powerups,
        )

        level.save()


init_db()
