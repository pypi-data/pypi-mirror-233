##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError

import pyodbc
from unskript.connectors.schema.ms_sql import MSSQLSchema
from unskript.connectors.interface import ConnectorInterface


class MSSQLConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            MsSQLCredential = MSSQLSchema(**data)
        except ValidationError as e:
            raise e

        try:
            if MsSQLCredential.User or MsSQLCredential.Password.get_secret_value():
                cnxn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + MsSQLCredential.Server + ';DATABASE=' + MsSQLCredential.DBName + ';UID=' + MsSQLCredential.User
                    + ';PWD=' + MsSQLCredential.Password.get_secret_value())
            else:
                cnxn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + MsSQLCredential.Server + ';DATABASE=' + MsSQLCredential.DBName)
        except pyodbc.Error as e:
            errString = 'Not able to connect to MSSQL, error {}'.format(str(e))
            print(errString)
            raise Exception(errString)
        return cnxn
