from flask_login import UserMixin
import models.database as db

class User(UserMixin): 
    def __str__(self) -> str:
        return "id : {0}".format(self.id)
    
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,id):
        self.__id = id

    @property
    def email(self):
        return self.__email
    @email.setter    
    def email(self,email):
        self.__email = email

    @property
    def country(self):
        return self.__country
    @country.setter    
    def country(self,country):
        self.__country = country

    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self,password):
        self.__password = password

    @property
    def name(self):
        return self.__name
    @name.setter    
    def name(self,name):
        self.__name = name

    @property
    def gender(self):
        return self.__gender
    @gender.setter    
    def gender(self,gender):
        self.__gender = gender

    @property
    def language(self):
        return self.__language
    @language.setter    
    def language(self,language):
        self.__language = language

    @property
    def city(self):
        return self.__city
    @city.setter    
    def city(self,city):
        self.__city = city
        
    @property
    def websocket_id(self):
        return self.__websocket_id
    @websocket_id.setter
    def websocket_id(self, websocket_id):
        self.__websocket_id = websocket_id