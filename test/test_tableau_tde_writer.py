import unittest

from tableausdkpy3 import *


class PyTableauTdeWriterTestCase(unittest.TestCase):
    TED_OUTPUT_PATH = 'tableau_tde_writter_test_output.tde'

    # def test_types_mapping(self):
    #     mapping = PYODBC_TDE_TYPE_MAPPING
    #     self.assertEqual(mapping[type('a str')], TableauType.UNICODE_STRING)
    #     # self.assertEqual(mapping[type(<bytes object>)], TableauType.CHAR_STRING) # TODO: check btyes object
    #     # self.assertEqual(mapping[type(<bytearray object>)], TableauType.CHAR_STRING) # TODO: bytearray object
    #     self.assertEqual(mapping[type(True)], TableauType.BOOLEAN)
    #     self.assertEqual(mapping[type(False)], TableauType.BOOLEAN)
    #     self.assertEqual(mapping[type(datetime.date(2018, 7, 12))], TableauType.DATE)
    #     self.assertEqual(mapping[type(datetime.time(10, 38, 47))], TableauType.DATETIME)
    #     # self.assertEqual(mapping[type(datetime.time(10, 38, 47, <tzone_info>))], TableauType.UNICODE_STRING) #TODO:
    #     self.assertEqual(mapping[type(datetime.datetime(2018, 7, 12, 10, 38, 47))], TableauType.DATETIME)
    #     # self.assertEqual(mapping[type(datetime.datetime(2018, 7, 12, 10, 38, 47, <tzone_info>))], TableauType.UNICODE_STRING) #TODO:
    #     self.assertEqual(mapping[type(decimal.Decimal.from_float(0.1))], TableauType.DOUBLE)
    #     self.assertEqual(mapping[type(decimal.Decimal.from_float(float('0.1')))], TableauType.DOUBLE)
    #     self.assertEqual(mapping[type(decimal.Decimal.from_float(float('nan')))], TableauType.DOUBLE)
    #     self.assertEqual(mapping[type(decimal.Decimal.from_float(float('inf')))], TableauType.DOUBLE)
    #     self.assertEqual(mapping[type(decimal.Decimal.from_float(-float('inf')))], TableauType.DOUBLE)
    #     self.assertEqual(mapping[type(UUID('{12345678-1234-5678-1234-567812345678}'))], TableauType.UNICODE_STRING)
    #     self.assertEqual(mapping[type(UUID('12345678123456781234567812345678'))], TableauType.UNICODE_STRING)

    def test_init_schema(self):
        out_path = PyTableauTdeWriterTestCase.TED_OUTPUT_PATH

        # clean up
        if os.path.exists(out_path):
            os.remove(out_path)

        df = pd.DataFrame(
            data={
                'StrColoumn': ['a string'],
                'BytesColoumn': [b'B'],
                'BytearrayColoumn': [
                    [b'B', b'A', b'M', b'R', b'i', b's', b'k', b'D', b'e', b'v']
                ],
                'BoolColoumn': [True],
                'DateColoumn': [datetime.date(2018, 7, 12)],
                'TimeColoumn': [datetime.time(10, 38, 47)],
                'IntColoumn': [1],  # TODO: test value that would be convert to long integer in C type
                'FloatColoumn': [12.10],
                'DecimalColoumn': [decimal.Decimal.from_float(float('0.1'))],
                'UuidColoumn': [UUID('12345678123456781234567812345678')],
            },
        )
        # , dtype=[str, bytes, bytearray, bool, datetime.date, datetime.time, datetime.datetime, int, float, decimal.Decimal, UUID]
        column_defs = [
            ExtractColumnDefinition('str_col', TableauType.UNICODE_STRING),
            ExtractColumnDefinition('bytes_col', TableauType.CHAR_STRING),
            ExtractColumnDefinition('bytearray_col', TableauType.CHAR_STRING),
            ExtractColumnDefinition('bool_col', TableauType.BOOLEAN),
            ExtractColumnDefinition('date_col', TableauType.DATE),
            ExtractColumnDefinition('time_col', TableauType.DATETIME),
            ExtractColumnDefinition('datetime_col', TableauType.DATETIME),
            ExtractColumnDefinition('int_col', TableauType.INTEGER),
            ExtractColumnDefinition('float_col', TableauType.DOUBLE),
            ExtractColumnDefinition('UUID_col', TableauType.UNICODE_STRING)
        ]
        df = df[['StrColoumn', 'BytesColoumn', 'BytearrayColoumn', 'BoolColoumn', 'DateColoumn', 'TimeColoumn',
                     'IntColoumn', 'FloatColoumn', 'DecimalColoumn', 'UuidColoumn']]
        writter = TableauTdeWriter(out_path)
        writter._init_schema(column_defs)

        col_def = writter.extract.openTable(TDE_TABLE_NAME).getTableDefinition()

        for i in range(col_def.getColumnCount()):
            self.assertEqual(col_def.getColumnType(i), column_defs[i].type)



    def test_set_value(self):
        # TODO:
        pass

    def test_write_df_to_tde(self):
        out_path = PyTableauTdeWriterTestCase.TED_OUTPUT_PATH

        # clean up
        if os.path.exists(out_path):
            os.remove(out_path)

        df = pd.DataFrame(
            data={
                'StrColoumn': ['a string'],
                'BytesColoumn': [b'B'.decode('ascii')],
                'BytearrayColoumn': [
                    b'BAMRiskDev'.decode('ascii')
                ],
                'BoolColoumn': [True],
                'DateColoumn': [datetime.date(2018, 7, 12)],
                'TimeColoumn': [datetime.datetime(1900, 1, 1,10, 38, 47)],
                'DateTimeColoumn': [datetime.datetime.today()],
                'IntColoumn': [1],  # TODO: test value that would be convert to long integer in C type
                'FloatColoumn': [12.10],
                'DecimalColoumn': [decimal.Decimal.from_float(float('0.1'))],
                'UuidColoumn': [str(UUID('12345678123456781234567812345678'))],
            })
        # , dtype=[str, bytes, bytearray, bool, datetime.date, datetime.time, datetime.datetime, int, float, decimal.Decimal, UUID]
        column_defs = [
            ExtractColumnDefinition('str_col', TableauType.UNICODE_STRING),
            ExtractColumnDefinition('bytes_col', TableauType.CHAR_STRING),
            ExtractColumnDefinition('bytearray_col', TableauType.CHAR_STRING),
            ExtractColumnDefinition('bool_col', TableauType.BOOLEAN),
            ExtractColumnDefinition('date_col', TableauType.DATE),
            ExtractColumnDefinition('time_col', TableauType.DATETIME),
            ExtractColumnDefinition('datetime_col', TableauType.DATETIME),
            ExtractColumnDefinition('int_col', TableauType.INTEGER),
            ExtractColumnDefinition('float_col', TableauType.DOUBLE),
            ExtractColumnDefinition('decimal_col', TableauType.DOUBLE),
            ExtractColumnDefinition('UUID_col', TableauType.UNICODE_STRING)
        ]

        # set fixed column order
        df = df[['StrColoumn', 'BytesColoumn', 'BytearrayColoumn', 'BoolColoumn',
                 'DateColoumn', 'TimeColoumn', 'DateTimeColoumn', 'IntColoumn',
                 'FloatColoumn', 'DecimalColoumn', 'UuidColoumn']]

        writter = TableauTdeWriter(out_path)
        writter.write_pandas_dataframe(df, column_defs)


    def test_write_pyodbc_cursor_result_to_tde(self):
        out_path = PyTableauTdeWriterTestCase.TED_OUTPUT_PATH

        # clean up
        if os.path.exists(out_path):
            os.remove(out_path)


        import pyodbc
        server = ''
        db = ''
        conn_str = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=' + server + ';DATABASE=' + db + ';Trusted_Connection=yes'

        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        q = ''

        writer = TableauTdeWriter(out_path)
        cursor.execute(q)
        writer.write_from_pyodbc_cursor(cursor)


    def test_apppend_mode(self):
        # TODO:
        pass


if __name__ == '__main__':
    unittest.main()

