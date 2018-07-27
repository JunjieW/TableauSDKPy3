# -----------------------------------------------------------------------
# Copyright (c) 2012 Tableau Software, Incorporated
#                    and its licensors. All rights reserved.
# Protected by U.S. Patent 7,089,266; Patents Pending.
#
# Portions of the code
# Copyright (c) 2002 The Board of Trustees of the Leland Stanford
#                    Junior University. All rights reserved.
# -----------------------------------------------------------------------
# HyperExtract.py
# -----------------------------------------------------------------------
# WARNING: Computer generated file.  Do not hand modify.

from ctypes import *
from . import Exceptions
from . import Libs
from . import StringUtils
from . import Types

libs = Libs.LoadLibs()
hyperExtract_lib = libs.load_lib('HyperExtract')

class TableDefinition(object):
    """Represents the schema for a table in a Tableau extract. The schema consists of a collection of column definitions, or more specifically name/type pairs."""

    def __init__(
        self
      , _handle = None
      , _parent = None
    ):
        """Initializes a new instance of the TableDefinition class.
        @param self The object pointer.
        """

        if _handle != None:
            self._handle = _handle
            self._parent = _parent
            return

        self._handle = c_void_p(None)

        ret = hyperExtract_lib.TabTableDefinitionCreate(
            byref(self._handle)
        )

        if int(ret) != int(Types.Result.SUCCESS):
            raise Exceptions.TableauException(ret, Exceptions.GetLastErrorMessage())

    def close(self):
        """Closes the TableDefinition object and frees associated memory.
        @param self The object pointer.
        """
        if self._handle != None:
            hyperExtract_lib.TabTableDefinitionClose( self._handle )
            self._handle = None

    def __del__(self):
        self.close()

    def getDefaultCollation(
        self
    ):
        """Returns the default collation for the table definition. The default is Collation.BINARY (0). You can change the default collation by calling <b>SetDefaultCollaction</b>.
        @param self The object pointer.
           @return The default collation.
        """

        retval = c_int()
        result = hyperExtract_lib.TabTableDefinitionGetDefaultCollation(
        self._handle
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return retval.value

    def setDefaultCollation(
        self
      , collation
    ):
        """Sets the default collation for new string columns.
        @param self The object pointer.
           @param collation The default collation for new string columns.
        """

        result = hyperExtract_lib.TabTableDefinitionSetDefaultCollation(
        self._handle
          , c_int(collation)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def addColumn(
        self
      , name
      , type
    ):
        """Adds a column to the table definition. The order in which columns are added specifies their column number. String columns are defined with the current default collation.
        @param self The object pointer.
           @param name The name of the column to add.
           @param type The data type of the column to add.
        """

        if name == None:
            raise ValueError('name must not be None')

        result = hyperExtract_lib.TabTableDefinitionAddColumn(
        self._handle
          , StringUtils.ToTableauString(name)
          , c_int(type)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def addColumnWithCollation(
        self
      , name
      , type
      , collation
    ):
        """Adds a column that has the specified collation.
        @param self The object pointer.
           @param name The name of the column to add.
           @param type The data type of the column to add.
           @param collation For string columns, the collation to use. For other types of columns, this value is ignored.
        """

        if name == None:
            raise ValueError('name must not be None')

        result = hyperExtract_lib.TabTableDefinitionAddColumnWithCollation(
        self._handle
          , StringUtils.ToTableauString(name)
          , c_int(type)
          , c_int(collation)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def getColumnCount(
        self
    ):
        """Returns the number of columns in the table definition.
        @param self The object pointer.
           @return The number of columns.
        """

        retval = c_int()
        result = hyperExtract_lib.TabTableDefinitionGetColumnCount(
        self._handle
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return retval.value

    def getColumnName(
        self
      , columnNumber
    ):
        """Returns the name of the specified column.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to return the name for.
           @return The column name.
        """

        retval = c_void_p(None)
        result = hyperExtract_lib.TabTableDefinitionGetColumnName(
        self._handle
          , c_int(columnNumber)
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return StringUtils.FromTableauString(retval)

    def getColumnType(
        self
      , columnNumber
    ):
        """Returns the data type of the specified column.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to return the name for.
           @return The column data type.
        """

        retval = c_int()
        result = hyperExtract_lib.TabTableDefinitionGetColumnType(
        self._handle
          , c_int(columnNumber)
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return retval.value

    def getColumnCollation(
        self
      , columnNumber
    ):
        """Returns the collation of the specified column.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to return the collation for.
           @return The column collation.
        """

        retval = c_int()
        result = hyperExtract_lib.TabTableDefinitionGetColumnCollation(
        self._handle
          , c_int(columnNumber)
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return retval.value

class Row(object):
    """Defines a row to be inserted into a table in an extract. The row is structured as a tuple."""

    def __init__(
        self
      , tableDefinition
    ):
        """Initializes a new instance of the Row class. This method creates an empty row that has the specified schema.
        @param self The object pointer.
           @param tableDefinition The schema to use.
        """

        self._handle = c_void_p(None)

        ret = hyperExtract_lib.TabRowCreate(
            byref(self._handle)
          , tableDefinition._handle
        )

        if int(ret) != int(Types.Result.SUCCESS):
            raise Exceptions.TableauException(ret, Exceptions.GetLastErrorMessage())

    def close(self):
        """Closes the row and frees associated resources.
        @param self The object pointer.
        """
        if self._handle != None:
            hyperExtract_lib.TabRowClose( self._handle )
            self._handle = None

    def __del__(self):
        self.close()

    def setNull(
        self
      , columnNumber
    ):
        """Sets the specified column in the row to null.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
        """

        result = hyperExtract_lib.TabRowSetNull(
        self._handle
          , c_int(columnNumber)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setInteger(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a 32-bit unsigned integer value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value The 32-bit integer value.
        """

        result = hyperExtract_lib.TabRowSetInteger(
        self._handle
          , c_int(columnNumber)
          , c_int(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setLongInteger(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a 64-bit unsigned integer value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value The 64-bit integer value.
        """

        if ( value <= -2**63 or value >= 2**63 ):
            raise Exceptions.TableauException(Types.Result.INVALID_ARGUMENT, "Value is out of range [-2^63+1, 2^63-1].")

        result = hyperExtract_lib.TabRowSetLongInteger(
        self._handle
          , c_int(columnNumber)
          , c_longlong(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setDouble(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a double value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value The double value.
        """

        result = hyperExtract_lib.TabRowSetDouble(
        self._handle
          , c_int(columnNumber)
          , c_double(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setBoolean(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a Boolean value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value True or false.
        """

        result = hyperExtract_lib.TabRowSetBoolean(
        self._handle
          , c_int(columnNumber)
          , c_bool(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setString(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a string value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value The string value.
        """

        if value == None:
            raise ValueError('value must not be None')

        result = hyperExtract_lib.TabRowSetString(
        self._handle
          , c_int(columnNumber)
          , StringUtils.ToTableauString(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setCharString(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a string value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value The string value.
        """

        if value == None:
            raise ValueError('value must not be None')
        # char strings are always ascii, required for py3
        value = value.encode('ascii')

        result = hyperExtract_lib.TabRowSetCharString(
        self._handle
          , c_int(columnNumber)
          , c_char_p(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setDate(
        self
      , columnNumber
      , year
      , month
      , day
    ):
        """Sets the specified column in the row to a date value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param year The year.
           @param month The month.
           @param day The day.
        """

        result = hyperExtract_lib.TabRowSetDate(
        self._handle
          , c_int(columnNumber)
          , c_int(year)
          , c_int(month)
          , c_int(day)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setDateTime(
        self
      , columnNumber
      , year
      , month
      , day
      , hour
      , min
      , sec
      , frac
    ):
        """Sets the specified column in the row to a datetime value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param year The year.
           @param month The month.
           @param day The day.
           @param hour The hour.
           @param min The minute.
           @param sec The second.
           @param frac The fraction of a second as one tenth of a millisecond (1/10000).
        """

        result = hyperExtract_lib.TabRowSetDateTime(
        self._handle
          , c_int(columnNumber)
          , c_int(year)
          , c_int(month)
          , c_int(day)
          , c_int(hour)
          , c_int(min)
          , c_int(sec)
          , c_int(frac)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setDuration(
        self
      , columnNumber
      , day
      , hour
      , minute
      , second
      , frac
    ):
        """Sets the specified column in the row to a duration value (time span).
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param day The number of days.
           @param hour The number of hours.
           @param minute The number of minutes.
           @param second The number of seconds.
           @param frac The fraction of a second as one tenth of a millisecond (1/10000).
        """

        result = hyperExtract_lib.TabRowSetDuration(
        self._handle
          , c_int(columnNumber)
          , c_int(day)
          , c_int(hour)
          , c_int(minute)
          , c_int(second)
          , c_int(frac)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def setSpatial(
        self
      , columnNumber
      , value
    ):
        """Sets the specified column in the row to a geospatial value.
        @param self The object pointer.
           @param columnNumber The column number (zero-based) to set a value for.
           @param value The spatial value (as a charString).
        """

        result = hyperExtract_lib.TabRowSetSpatial(
        self._handle
          , c_int(columnNumber)
          , c_char_p(value)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

class Table(object):
    """Represents a data table in the extract."""

    def insert(
        self
      , row
    ):
        """Queues a row for insertion into the table. This method might insert a set of buffered rows.
        @param self The object pointer.
           @param row The row to insert.
        """

        result = hyperExtract_lib.TabTableInsert(
        self._handle
          , row._handle
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    def getTableDefinition(
        self
    ):
        """Gets the table's schema.
        @param self The object pointer.
           @return A copy of the table's schema, which must be closed.
        """

        retval = c_void_p(None)
        result = hyperExtract_lib.TabTableGetTableDefinition(
        self._handle
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return TableDefinition( _handle = retval, _parent = self)

    def __init__(self, _handle, _parent):
        """Internal use only: Create a new instance to wrap the specified handle."""
        self._handle = _handle
        self._parent = _parent

class Extract(object):
    """Represents a Tableau data engine database."""

    def __init__(
        self
      , path
    ):
        """Initializes an extract object using a file system path and file name. If the extract file already exists, this method opens the extract. If the file does not already exist, the method initializes a new extract. You must explicitly close this object in order to save the extract to disk and release its resources.
        @param self The object pointer.
           @param path The path and file name of the extract file to create or open. The path must include the ".hyper" extension.
        """

        self._handle = c_void_p(None)

        if path == None:
            raise ValueError('path must not be None')

        ret = hyperExtract_lib.TabExtractCreate(
            byref(self._handle)
          , StringUtils.ToTableauString(path)
        )

        if int(ret) != int(Types.Result.SUCCESS):
            raise Exceptions.TableauException(ret, Exceptions.GetLastErrorMessage())

    def close(self):
        """Closes the extract and any open tables that it contains. You must call this method in order to save the extract to a .hyper file and to release its resources.
        @param self The object pointer.
        """
        if self._handle != None:
            hyperExtract_lib.TabExtractClose( self._handle )
            self._handle = None

    def __del__(self):
        self.close()

    def addTable(
        self
      , name
      , tableDefinition
    ):
        """Adds a table to the extract.
        @param self The object pointer.
           @param name The name of the table to add. Currently, this method can only add a table named "Extract".
           @param tableDefinition The schema of the new table.
           @return A reference to the table.
        """

        if name == None:
            raise ValueError('name must not be None')

        retval = c_void_p(None)
        result = hyperExtract_lib.TabExtractAddTable(
        self._handle
          , StringUtils.ToTableauString(name)
          , tableDefinition._handle
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return Table( _handle = retval, _parent = self)

    def openTable(
        self
      , name
    ):
        """Opens the specified table in the extract.
        @param self The object pointer.
           @param name The name of the table to open. Currently, this method can only open a table named "Extract".
           @return A reference to the table.
        """

        if name == None:
            raise ValueError('name must not be None')

        retval = c_void_p(None)
        result = hyperExtract_lib.TabExtractOpenTable(
        self._handle
          , StringUtils.ToTableauString(name)
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return Table( _handle = retval, _parent = self)

    def hasTable(
        self
      , name
    ):
        """Determines whether the specified table exists in the extract.
        @param self The object pointer.
           @param name The name of the table.
           @return True if the specified table exists; otherwise, false.
        """

        if name == None:
            raise ValueError('name must not be None')

        retval = c_bool()
        result = hyperExtract_lib.TabExtractHasTable(
        self._handle
          , StringUtils.ToTableauString(name)
          , byref(retval)
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

        return retval.value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

class ExtractAPI(object):
    """Provides management functions for the Extract API."""

    @staticmethod
    def initialize(
    ):
        """Initializes the Extract API. Calling this method is optional. The call initializes logging in the TableauSDKExtract.log file. If you call this method, you must call it before calling any other method for the Extract API.
        @param self The object pointer.
        """

        result = hyperExtract_lib.TabExtractAPIInitialize(
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())

    @staticmethod
    def cleanup(
    ):
        """Shuts down the Extract API. This call is required only if you previously called the Initialize method.
        @param self The object pointer.
        """

        result = hyperExtract_lib.TabExtractAPICleanup(
        )

        if result != Types.Result.SUCCESS:
            raise Exceptions.TableauException(result, Exceptions.GetLastErrorMessage())
