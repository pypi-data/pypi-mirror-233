##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError

## importing 'mysql.connector' as mysql for convenient
import mysql.connector as mysql

from unskript.connectors.schema.mysql import MySQLSchema
from unskript.connectors.interface import ConnectorInterface

class MySQLConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            mySQLCredential = MySQLSchema(**data)
        except ValidationError as e:
            raise e

        try:
            conn = mysql.connect(database=mySQLCredential.DBName,
                user=mySQLCredential.User,
                password=mySQLCredential.Password.get_secret_value(),
                host=mySQLCredential.Host,
                port=mySQLCredential.Port)
        except mysql.Error as e:
            errString = 'Not able to connect to MySQL, error {}, code {}'.format(e.msg, e.errno)
            print(errString)
            raise Exception(errString)
        return conn