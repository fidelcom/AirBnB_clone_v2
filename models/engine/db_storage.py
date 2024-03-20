#!/usr/bin/python3
"""This module defines a new engine DBStorage"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel


class DBStorage:
    """This class represents DBStorage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the class DBStorage"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(getenv('HBNB_MYSQL_USER'),
                        getenv('HBNB_MYSQL_PWD'),
                        getenv('HBNB_MYSQL_HOST'),
                        getenv('HBNB_MYSQL_DB')),
                pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadate.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session all objects
        depending of the class name"""
        if cls is None:
