import pymysql.cursors
from pymysql.err import InternalError


class DBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    def __init__(self):
        DBManager.createDB()
        DBManager.createUniv()
        return

    @staticmethod
    def createDB():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               charset='utf8mb4')
        try:
            with conn.cursor() as cursor:
                sql = 'USE sookmyung'
                cursor.execute(sql)
        except InternalError:
            with conn.cursor() as cursor:
                sql = 'CREATE DATABASE IF NOT EXISTS sookmyung'
                cursor.execute(sql)
        finally:
            conn.commit()
        return

    @staticmethod
    def createUniv():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = '''
                       CREATE TABLE IF NOT EXISTS univ( 
                        id int(11) NOT NULL,
                        category varchar(50) NOT NULL,
                        division varchar(50) NOT NULL, 
                        title varchar(200) NOT NULL,
                        content varchar(20000),
                        view int(10),
                        date Date
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                '''
            cursor.execute(sql)
        return


    @staticmethod
    def insert(record):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'INSERT INTO univ (id, category, division, title, content,view,date) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (record.id, record.category, record.division, record.title, record.content,record.view,record.date))
        conn.commit()
        return

    @staticmethod
    def select():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM univ'
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                print(row)
        return

    @staticmethod
    def delete_all():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'DELETE FROM univ'
            cursor.execute(sql)
            conn.commit()
        return