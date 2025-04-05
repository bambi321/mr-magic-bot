import sqlite3

class MagicDatabaseManager():

    def __init__(self, errorManager, logger, databasePath):
        self._error = errorManager
        self._logger = logger
        self.__database = self.__connectToDatabase(databasePath)

    # ----- PRIVATE METHODS -----

    def __connectToDatabase(self, path):
        try:
            return sqlite3.connect(path)
        except Exception as error:
            self._error.processError(f"Could not connect to database @ {path}", error)        
            return None

    def __actionQuery(self, query, fetchAll = False):

        data = []
        cur = self.__database.cursor()
        cur.execute(query)

        if fetchAll:
            data = cur.fetchall()

        cur.close()
        self.__database.commit()
        return data

    def __tableExists(self, tableName):
        try:
            self.__actionQuery(f'select * from {tableName}')
            return True
        except Exception as error:
            return False

    # ----- PROTECTED METHODS -----

    def _dropTable(self, tableName):
        try:
            self.__actionQuery(f'drop table {tableName}')
            return self._error.SUCCESS
        except Exception as error:
            self._error.processError(f"Could not drop {tableName}", error)
            return self._error.FAILURE

    def _createTable(self, tableName, tableType):
        if self.__tableExists(tableName):
            self._dropTable(tableName)

        try :
            self.__actionQuery(f'create table {tableName} {tableType}')
            return self._error.SUCCESS
        except Exception as error:
            self._error.processError(f"Could not create table ({tableName})", error)
            return self._error.FAILURE

    def _insertValue(self, tableName, valuesTuple):
        try:
            self.__actionQuery(f'insert into {tableName} values {valuesTuple}')
            return self._error.SUCCESS
        except Exception as error:
            self._error.processError(f"Could not insert {valuesTuple} into {tableName}", error)
            return self._error.FAILURE

    def _collectValues(self, tableName):
        try:
            return self.__actionQuery(f'select * from {tableName}', True)
        except Exception as error:
            self._error.processError(f"Could not fetch results from {tableName}", error)
            return []

