import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserData(Base):
    '''
    This class is to create user table,
    it takes declarative base object as parameter.
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    photo = Column(String(255))

    @property
    def serialize(self):
        ''' Return data as object in simple serializeable format'''
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'photo': self.picture,
        }


class Brand(Base):
    '''
    This class is to create brand table,
    it takes declarative base object as parameter.
    '''
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(50), nullable=False)

    user = relationship(UserData)

    @property
    def serialize(self):
        ''' Return data as object in simple serializeable format'''
        return {
            'name': self.name,
            'id': self.id,

        }


class ModelName(Base):
    '''
    This class is to create model table,
    it takes declarative base object as parameter.
    '''
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    modelname = Column(String(30), nullable=False)
    brands = Column(String(30))
    modelnumber = Column(String(30))
    ctype = Column(String(30))
    colors = Column(String(30))
    wifi = Column(String(30))
    facedetection = Column(String(30))
    pixels = Column(String(50))
    builtinflash = Column(String(30))
    videoformat = Column(String(30))
    price = Column(String(20))
    description = Column(String(500))
    picture = Column(String(500))

    brand = relationship(Brand)
    user = relationship(UserData)

    @property
    def serialize(self):
        ''' Return data as object in simple serializeable format'''
        return {

            'id': self.id,
            'modelname': self.modelname,
            'brands': self.brands,
            'modelnumber': self.modelnumber,
            'ctype': self.ctype,
            'colors':  self.colors,
            'wifi': self.wifi,
            'facedetection': self.facedetection,
            'pixels': self.pixels,
            'builtinflash': self.builtinflash,
            'videoformat': self.videoformat,

            'price': self.price,
            'description': self.description,
            'picture': self.picture,

        }

engine = create_engine('sqlite:///camcatalog.db')
Base.metadata.create_all(engine)
