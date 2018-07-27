import unittest

from tableausdkpy3 import *



class ExtractAndTypesTestCase(unittest.TestCase):
    def setUp(self):
        # file path to output std
        self.filename = 'test_out.tde'

        # Initialize Tableau SDK Extract API
        ExtractAPI.initialize()

    def tearDown(self):
        # Close the Tableau Extract API
        ExtractAPI.cleanup()


    def test_create_or_open_extract(self):
        """
        Create Extract (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
        The test data and schema is based on the official Tableau SDK python samples
        """
        try:
            # Create Extract Object
            # (NOTE: The Extract constructor opens an existing extract with the
            #  given filename if one exists or creates a new extract with the given
            #  filename if one does not)
            extract = Extract(self.filename)

            # Define Table Schema (If we are creating a new extract)
            # (NOTE: In Tableau Data Engine, all tables must be named 'Extract')
            if (not extract.hasTable('Extract')):
                schema = TableDefinition()
                schema.setDefaultCollation(Collation.EN_GB)
                schema.addColumn('Purchased', Type.DATETIME)
                schema.addColumn('Product', Type.CHAR_STRING)
                schema.addColumn('uProduct', Type.UNICODE_STRING)
                schema.addColumn('Price', Type.DOUBLE)
                schema.addColumn('Quantity', Type.INTEGER)
                schema.addColumn('Taxed', Type.BOOLEAN)
                schema.addColumn('Expiration Date', Type.DATE)
                schema.addColumnWithCollation('Produkt', Type.CHAR_STRING, Collation.DE)
                schema.addColumn('Destination', Type.SPATIAL)
                table = extract.addTable('Extract', schema)
                if (table == None):
                    raise Exception('A fatal error occurred while creating the table:\nExiting now\n.')

            extract.close()

        except TableauException as e:
            print('A fatal error occurred while creating the new extract:\n', e, '\nExiting now.')
            exit(-1)




    def test_populateExtract(self):
        """
        Test creating all available types in an Tableau Extract, if None, default will be used.
        The test data and schema is based on the official Tableau SDK python samples.
        """
        try:
            extract = Extract(self.filename)

            # Get Schema
            table = extract.openTable('Extract')
            schema = table.getTableDefinition()

            # Insert Data
            row = Row(schema)
            row.setDateTime(0, 2012, 7, 3, 11, 40, 12, 4550)  # Purchased
            row.setCharString(1, 'Beans')  # Product
            row.setString(2, u'uniBeans')  # Unicode Product
            row.setDouble(3, 1.08)  # Price
            row.setDate(6, 2029, 1, 1)  # Expiration Date
            row.setCharString(7, 'Bohnen')  # Produkt
            for i in range(10):
                row.setInteger(4, i * 10)  # Quantity
                row.setBoolean(5, i % 2 == 1)  # Taxed
                row.setSpatial(8, "POINT (30 10)")  # Destination
                table.insert(row)

            extract.close()

        except TableauException as e:
            print('A fatal error occurred while populating the extract:\n', e, '\nExiting now.')
            exit(-1)


if __name__ == '__main__':
    unittest.main()