from dateutil import parser as dateutil_parser
import pandas as pd

from .Extract import *
from .Types import Collation as TableauCollation
from .Types import Type as TableauType

import datetime
import decimal
from uuid import UUID

# (NOTE: In Tableau Data Engine, all tables must be named 'Extract')
#  According to the Tableau SDK documentation
TDE_TABLE_NAME = 'Extract'

# NOTE: this mapping should cover all the data types returned by pyodbc - the interface used by bamdata api
# All types returned from pyodbc: https://github.com/mkleehammer/pyodbc/wiki/Data-Types
# IF THE ODBC ACCESS MODEUL CHANGED, THIS MAPPING SHOULD UPDATE ACCORDINGLY
PYODBC_TDE_TYPE_MAPPING = {
    # None: type(None),
    str: TableauType.UNICODE_STRING,
    bytes: TableauType.CHAR_STRING, #TODO: need to verify
    bytearray: TableauType.CHAR_STRING, # need to verify
    bool: TableauType.BOOLEAN,
    datetime.date: TableauType.DATE,  #TODO: need to verify
    datetime.time: TableauType.DATETIME, #TODO: need to verify
    datetime.datetime: TableauType.DATETIME,
    int: TableauType.INTEGER,
    float: TableauType.DOUBLE,  #TODO: need to verify
    decimal.Decimal: TableauType.DOUBLE,
    UUID: TableauType.UNICODE_STRING  #TODO: need to verify
}

# Default map of TSQL types to Tableau types
# https://docs.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-2017
TSQL_TDE_TYPE_MAPPING = {
    'bigint': TableauType.DOUBLE,
    'bit': TableauType.INTEGER,
    'decimal': TableauType.DOUBLE,
    'int': TableauType.INTEGER,
    'smallint': TableauType.INTEGER,
    'tinyint': TableauType.INTEGER,
    # 'money': '',
    # 'numeric': '',
    # 'smallmoney': '',
    'float': TableauType.DOUBLE,
    'real': TableauType.DOUBLE,
    'date': TableauType.DATE,
    # 'datetimeoffset': '',
    # 'datetime2': '',
    'datetime': TableauType.DATETIME,
    # 'smalldatetime': TableauType.DATETIME,
    # 'time': '',
    'char': TableauType.CHAR_STRING,
    'varchar': TableauType.CHAR_STRING,
    # 'text': '',
    'nchar': TableauType.UNICODE_STRING,
    'nvarchar': TableauType.UNICODE_STRING,
    'ntext': TableauType.UNICODE_STRING,
    # 'binary': '',
    # 'image': '',
    # 'varbinary': ''
    # cursor etc. not support
}



class ExtractColumnDefinition(object):
    def __init__(self, name, type, collation=None):
        """
        Tableau Extract column definition class
        :param name: str name of the column
        :param type: python type object
        :param collation: None of one of the collation supported by Tableau SDK - tableausdkpy3.Types.Collation
        """
        self.name = name
        self.type = type
        self.collation = collation if (collation is not None) and (collation in dir(TableauCollation)) else None

class TableauTdeWriter(object):

    def __init__(self, path):
        ExtractAPI.initialize()
        self.path = path
        self.extract = Extract(self.path)
        self.schema = None

    # def __del__(self):
    #     ExtractAPI.cleanup()


    def _init_schema(self, column_defs):
        # TODO: if update to pandas >=0.21.0, can do type_infer if column_defs not specified
        schema = TableDefinition()
        for col in column_defs:
            if col.collation is None:
                schema.addColumn(col.name, col.type)
            else:
                schema.addColumnWithCollation(col.name, col.type, col.collation)

        self.extract.addTable(TDE_TABLE_NAME, schema)
        self.schema = schema


    def _set_value(self, tab_row, cidx, value):
        """
        Set value at column with index cidx  in a Tableau Row object.
        :param tab_row: Tableau Row object
        :param cidx: the column index, zero based
        :param value: the value to set
        :return: void
        """
        # schema = self.extract.openTable(TDE_TABLE_NAME).getTableDefinition()
        col_type = self.schema.getColumnType(cidx)
        # check None and NaN
        if pd.isnull(value):
            tab_row.setNull(cidx)
            return

        # TODO: make it more flexible when tableau types expand
        if col_type == TableauType.UNICODE_STRING:
            tab_row.setString(cidx, str(value))
        elif col_type == TableauType.CHAR_STRING:
            tab_row.setCharString(cidx, str(value))
        elif col_type == TableauType.BOOLEAN:
            tab_row.setBoolean(cidx, bool(value))
        elif col_type == TableauType.INTEGER:
            # TODO: shouldn't have done this to default to LongInteger
            tab_row.setLongInteger(cidx, int(value))
        elif col_type == TableauType.DOUBLE:
            tab_row.setDouble(cidx, float(value))
        elif col_type == TableauType.DATE:
            dt = value
            if not isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
                # raise TypeError('an datetime.date or datetime.datetime is required (got {})'.format(type(dt)))
                dt = dateutil_parser.parse(dt)
            tab_row.setDate(cidx, dt.year, dt.month, dt.day)
        elif col_type == TableauType.DATETIME:
            dt = value
            if not isinstance(dt, datetime.datetime):
                # raise TypeError('an datetime.datetime is required (got {})'.format(type(dt)))
                dt = dateutil_parser.parse(dt)
            # TODO: WARNNING lost precision of micorsec when casting into fraction sec
            tab_row.setDateTime(cidx, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond // 100)
        elif col_type == TableauType.SPATIAL:
            # TODO: implement convert_to_spatial() to convert into Tableau Spatial object
            # row.setSpatial(cidx, convert_to_spatial(value))
            raise NotImplementedError('To Implement')
        elif col_type == TableauType.DURATION:
            td = datetime.timedelta(value)
            if not isinstance(td, datetime.timedelta):
                raise TypeError('an datetime.timedelta is required (got {})'.format(type(td)))
            td_hours = td.seconds / 3600
            td_minutes = td.seconds % 3600 / 60
            td_sec = td.seconds % 60
            # TODO: WARNNING the micorsec precision get lost when casting into fraction sec
            tab_row.setDuration(cidx, td.days, td_hours, td_minutes, td_sec, td.microseconds // 100)


    def write_pandas_dataframe(self, df, column_defs, append=False):
        """
        Write a pandas DataFrame to Tableau Extract with column_defs to set up its schema
        :param df: pandas DataFrame
        :param column_defs: list of ExtractColumnDefinition objects
        """
        if not self.extract.hasTable(TDE_TABLE_NAME):
            self._init_schema(column_defs)

        table = self.extract.openTable(TDE_TABLE_NAME)
        schema = table.getTableDefinition()

        if not self.schema:
            self.schema = schema


        for i, df_row in df.iterrows():
            tab_row = Row(schema)
            for j in range(df_row.count()):
                try:
                    value = df.iloc[i, j]
                    self._set_value(tab_row, j, value)
                except Exception as ex:
                    # TODO: log.ERROR(ridx, cidx, column type, column name)
                    print('ridx={}, cidx={}, colname={}, coltype={}, value={}, valuetype={}'.format(
                          i, j, schema.getColumnType(j), schema.getColumnName(j), df.iloc[i, j], type(df.iloc[i, j])))
                    raise ex
            table.insert(tab_row)
            tab_row.__del__()

        self.extract.close()
        ExtractAPI.cleanup()


    def write_from_pyodbc_cursor(self, cursor, append=False):
        """
        Write data from the result of executing query by pyodbc cursor. It's the caller's responsibility
        to release the cursor passed in.
        NOTE: to be able to parse date, datetime type from SQL correctly, the connection of cursor should use explicitly
              use SQLServer Native Client or ODBC Driver. See: https://stackoverflow.com/a/7196251/9195736
        :param cursor: a DB cursor can
        :param query:
        :return: void
        """
        import pyodbc
        if type(cursor) is not pyodbc.Cursor:
            raise ArgumentError(
                'Expecting cursor is not an object of {} but {}.'.format(pyodbc.Cursor, type(cursor)))

        row = cursor.fetchone()
        db_col_name_in_order = [a_col_tuple[0] for a_col_tuple in row.cursor_description]

        if not self.extract.hasTable(TDE_TABLE_NAME):
            colname_pytype_map = {item[0]: item[1] for item in list(cursor.description)}
            column_defs = []
            for col_name in db_col_name_in_order:
                tab_col_type = PYODBC_TDE_TYPE_MAPPING[colname_pytype_map[col_name]]
                extract_col_def = ExtractColumnDefinition(name=col_name, type=tab_col_type)
                column_defs.append(extract_col_def)
            self._init_schema(column_defs)

        # TODO: if append mode, check if the column definition matched

        if not row:
            # TODO: logger.warning('query return empty result, no data written')
            return

        # TODO: check auto commit
        # if not cursor.connection.autocommit:
        #     cursor.commit()

        table = self.extract.openTable(TDE_TABLE_NAME)
        schema = table.getTableDefinition()

        if not self.schema:
            self.schema = schema

        row_idx = -1
        while row:
            tab_row = Row(self.schema)
            row_idx += 1
            for col_idx in range(len(row)):
                try:
                    cell_value = row[col_idx]
                    self._set_value(tab_row, col_idx, cell_value)
                except Exception as ex:
                    # TODO: log.ERROR(...)
                    print('ridx={}, cidx={}, colname={}, coltype={}, value={}, valuetype={}'.format(
                        row_idx, col_idx, schema.getColumnName(col_idx), schema.getColumnType(col_idx), cell_value, type(cell_value)
                    ))
                    raise ex
            table.insert(tab_row)

            # TODO: check if Tableau API releases the row object by GC or until Extact close()
            #       if it's necessary to wait until Extract closed, we can save memory by manually release it
            # tab_row.__del__()

            row = cursor.fetchone()

        self.extract.close()
        ExtractAPI.cleanup()



# class TableauTdeReader(object):
#     def __init__(self, path):
#         pass
#
#     def __del__(self):
#         pass
#
#     def write_dataframe(self, append=True):
#         pass


# if __name__ == '__main__':
#     pass