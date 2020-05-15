# -*- coding: utf-8 -*-
from __future__ import print_function # if using python 2
import logging
from DB_Logger import dbHandler

if __name__ == "__main__":

    myh = dbHandler({''
                     'database_type': "sqlite",  # указать postgres или  sqlite
                     'db_file_path' : "testdatabase.db", #@ToDo сделать указание в kwargs, приходится пока указывать этот
                     'host': "192.168.224.128",
                     'user': "tester",
                     'password': "5",
                     'database': "tester",
                     'logtable_name': "test_log"
                     })
    l = logging.getLogger("Logger_Name")
    l.setLevel(logging.DEBUG)
    l.addHandler(myh)
    print('Your db is: ' +myh.database_type)
    while 1:
        l.info("Test info record into log table: \"" + myh.logtable_name + "\" was created...")
        print("Test info record into log table: \"" + myh.logtable_name + "\" was created...")
        l.debug("Test debug record into log table: \"" + myh.logtable_name + "\" was created...")
        print("Test debug record into log table: \"" + myh.logtable_name + "\" was created...")
        l.error("Test error record into log table: \"" + myh.logtable_name + "\" was created...")
        print("Test error record into log table: \"" + myh.logtable_name + "\" was created...")

        # Test exception and error logging - success
        try:
            1 / 0
        except ZeroDivisionError as e:
            l.exception(e, exc_info=True)  # log exception info at FATAL log level
            #l.error(e)
            #l.error(e, exc_info=True)  # log exception info at FATAL log level
            #l.fatal(e, exc_info=True)  # log exception info at FATAL log level
            #l.error(e, exc_info=True)
