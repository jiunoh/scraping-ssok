from UnivDBManager import UnivDBManager
from DBManager import DBManager
from DepartmentDBManager import DepartmentDBManager
from json_reader import read_wiz

class Main:
    def __init__(self):
        UnivDBManager()
        DepartmentDBManager()
        return

start = Main()
read_wiz()