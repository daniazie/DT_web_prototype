import pymysql

class DataBase:
    def __init__(self):
        try :
            self.db = pymysql.connect(
                host = '34.64.35.60',
                user = 'root',   
                password = 'design1!',
                database = 'dt',
                cursorclass = pymysql.cursors.DictCursor
                )        
            self.cursor = self.db.cursor()

        except Exception as e:
            return ('접속오류', e)
        
    def __del__(self):
        if self.db:
            self.db.close()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            return row
        except:
            return None