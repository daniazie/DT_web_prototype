import pymysql

class DataBase:
    def __init__(self):
        try :
            self.__db = pymysql.connect(
                host = '34.64.35.60',
                user = 'root',   
                password = 'design1!',
                database = 'dt',
                cursorclass = pymysql.cursors.DictCursor
                )        
            self.__cursor = self.__db.cursor()

        except Exception as e:
            return ('접속오류', e)
        
    def __del__(self):
        if self.__db:
            self.__db.close()

    def execute_select(self, sql):
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row
        except:
            return None
        
    def execute_else(self, sql):
        self.__cursor.execute(sql)
        self.__db.commit()
