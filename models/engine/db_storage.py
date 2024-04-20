#!/usr/bin/python3
"""Contains storage for database (not file storage)"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv

from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

ENV = getenv("HBNB_ENV")
DB_USER = getenv("HBNB_MYSQL_USER")
DB_PSWD = getenv("HBNB_MYSQL_PWD")
DB_HOST = getenv("HBNB_MYSQL_HOST")
DB_NAME = getenv("HBNB_MYSQL_DB")
STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")


class DBStorage:
    """DataBase Storage Engine"""
    __engine = None
    __session = None
    __classes = {User, Place, State, City, Review, Amenity}

    def __init__(self):
        """Initializes the database engine."""

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                DB_USER,
                DB_PSWD,
                DB_HOST,
                DB_NAME
            ),
            pool_pre_ping=True
        )

        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in database"""
        all_db_rows = {}
        classes = self.__classes

        if cls is None:
            for clname in classes:
                for instance in self.__session.query(clname).all():
                    key = f"{clname.__name__}.{instance.id}"
                    all_db_rows[key] = instance
        else:
            for instance in self.__session.query(cls):
                key = f"{cls.__name__}.{instance.id}"
                all_db_rows[key] = instance
        return all_db_rows

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes from the current database session obj if not None
        """
        if obj is not None:
            self.__session(obj)

    def reload(self):
        """
        Creates all tables in the database
        Create the current database session by using a sessionmaker
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Removes session"""
        self.__session.close()