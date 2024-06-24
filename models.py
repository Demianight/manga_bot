from peewee import (BigAutoField, BigIntegerField, CharField, ForeignKeyField,
                    Model, SqliteDatabase)

database = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = BigAutoField()
    tg_id = BigIntegerField()


class Manga(BaseModel):
    id = CharField()
    title = CharField()
    url = CharField()


class FavoriteManga(BaseModel):
    id = BigAutoField()
    user = ForeignKeyField(User, backref="favorite_mangas")
    manga = ForeignKeyField(Manga, backref="in_favorite_of")


database.create_tables([User, Manga, FavoriteManga])
