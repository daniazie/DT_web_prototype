from flask_login import UserMixin
import models.database as db

class User(UserMixin): 
    def pull_info_from_database_by_id(self, user_id):
        connection = db.DataBase()
        result = connection.execute_select("SELECT * FROM User WHERE id='{0}'".format(user_id))
        if result: 
            self.__id = result['id']
            self.__password = result['password']
            self.__name = result['name']
            return True
        else: # failed to search id from database
            return False

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
    @name.setter    
    def city(self,city):
        self.__city = city