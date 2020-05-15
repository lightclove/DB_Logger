# -*- coding: utf-8 -*-
from __future__ import print_function # if using python 2
import logging
import sqlite3
import time

########################################################################################################################
# Logging handler for PostgreSQL, sqlite
class dbHandler(logging.Handler):

    def connect(self):
        try:
            if self.database_type == 'postgres':
                import psycopg2
                self.__connect = psycopg2.connect(
                    database=self.__database,
                    host=self.__host,
                    user=self.__user,
                    password=self.__password,
                    sslmode="disable")
            elif self.database_type == 'sqlite':
                self.__connect = sqlite3.connect(self.db_file_path)

            return True
        except:
            return False
            ########################################################################################################################

    def __init__(self, params):
        if not params:
            raise Exception("No database where to log ☻")
        self.db_file_path = params['db_file_path'] # for the sqlite file.db
        self.database_type = params['database_type']
        self.__database = params['database']
        self.__host = params['host']
        self.__user = params['user']
        self.__password = params['password']
        self.__connect = None
        self.logtable_name = params['logtable_name']

        if not self.connect():
            raise Exception("Database connection error ☻")
        logging.Handler.__init__(self)
        self.__initial_sql = """CREATE TABLE IF NOT EXISTS """ + self.logtable_name + """ (
                                   Created text,
                                   Name text,
                                   LogLevel text,
                                   LogLevelName text,
                                   Message text,
                                   Module text,
                                   FuncName text,
                                   LineNo text,
                                   Exception text,
                                   Process text,
                                   Thread text,
                                   ThreadName text
                              )"""
        if self.database_type == 'postgres':
            self.__insertion_sql = """INSERT INTO """ + self.logtable_name + """(
                                           Created,
                                           Name,
                                           LogLevel,
                                           LogLevelName,
                                           Message,
                                           Module,
                                           FuncName,
                                           LineNo,
                                           Exception,
                                           Process,
                                           Thread,
                                           ThreadName)
                                           VALUES(
                                           to_timestamp(%(created)s),
                                           %(name)s,
                                           %(levelno)s,
                                           %(levelname)s,
                                           %(message)s,
                                           %(module)s,
                                           %(funcName)s,
                                           %(lineno)s,
                                           %(exc_text)s,
                                           %(process)s,
                                           %(thread)s,
                                           %(threadName)s
                                   );"""
        elif self.database_type == 'sqlite':
            self.__insertion_sql = """INSERT INTO """ + self.logtable_name + """(
                                           Created,
                                           Name,
                                           LogLevel,
                                           LogLevelName,
                                           Message,
                                           Module,
                                           FuncName,
                                           LineNo,
                                           Exception,
                                           Process,
                                           Thread,
                                           ThreadName
                                           )
                                           VALUES(
                                           '%(created)s', 
                                           '%(name)s', 
                                           '%(levelno)s', 
                                           '%(levelname)s', 
                                           '%(message)s', 
                                           '%(module)s', 
                                           '%(funcName)s', 
                                           '%(lineno)s', 
                                           '%(exc_text)s', 
                                           '%(process)s', 
                                           '%(thread)s', 
                                           '%(threadName)s'
                                   );"""
        #elif self.__database_type == 'mysql':
        #...
        #elif self.__database_type == 'oracle':
        # ...

        #self.__drop_sql = "DROP TABLE " + self.logtable_name
        #self.__deletion_sql = "DELETE FROM "
        self.__connect.cursor().execute(self.__initial_sql)
        self.__connect.commit()
        self.__connect.cursor().close()
    ########################################################################################################################
    # for the sqlite3 time formatting
    def format_time(self, record):
        """
        Create a time stamp
        """
        record.created = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(record.created))

    ########################################################################################################################

    def emit(self, record):
        # Use default formatting:
        self.format(record)
        # for sqlite3
        if self.database_type == 'sqlite': self.format_time(record)

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            #record.exc_text = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        else:
            record.exc_text = ""
        try:
            # cur =  self.__connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur = self.__connect.cursor()
        except:
            self.connect()
            cur = self.__connect.cursor()
        try:
            #cur.execute(self.drop_sql) # Optionally drop table for some reasons, may be useful
            #cur.execute(self.deletion_sql) # Optionally clearing table before logging
            # Insert the log record:
            if self.database_type == 'postgres': cur.execute(self.__insertion_sql, record.__dict__)
            if self.database_type == 'sqlite': cur.execute(self.__insertion_sql % record.__dict__, record.__dict__)
        except BaseException as ie:
            print(str(ie))
        self.__connect.commit()
        self.__connect.cursor().close()
########################################################################################################################




