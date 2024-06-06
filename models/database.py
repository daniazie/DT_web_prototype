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

    def execute_select_one(self, sql):
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row
        except Exception as e:
            print(e)
            return None
        
    def execute_select_all(self, sql):
        try:
            self.__cursor.execute(sql)
            rows = self.__cursor.fetchall()
            return rows
        except Exception as e:
            print(e)
            return None
        
    def count_select_rows(self, sql):
        try:
            self.__cursor.execute(sql)
<<<<<<< HEAD
            rows = self.__cursor.fetchall(n) # type: ignore
=======
            rows = self.__cursor.fetchall()
>>>>>>> ade23fe966ba49c3f00fa1822e0947117ffe9362
            return len(rows)
        except Exception as e:
            print(e)
            return -1
        
    def execute_with_commit(self, sql):
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return True, None
        except Exception as e:
            print(e)
            return False, e
