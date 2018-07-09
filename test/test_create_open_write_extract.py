import argparse
import sys
import textwrap

from tableausdkpy3 import *
from tableausdkpy3.Extract import *
# from tableausdkpy3.Server import *

# ------------------------------------------------------------------------------
#   Create Extract
# ------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def createOrOpenExtract(filename, useSpatial):
    try:
        # Create Extract Object
        # (NOTE: The Extract constructor opens an existing extract with the
        #  given filename if one exists or creates a new extract with the given
        #  filename if one does not)
        extract = Extract(filename)

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
            if (useSpatial):
                schema.addColumn('Destination', Type.SPATIAL)
            table = extract.addTable('Extract', schema)
            if (table == None):
                print('A fatal error occurred while creating the table:\nExiting now\n.')
                exit(-1)

    except TableauException as e:
        print('A fatal error occurred while creating the new extract:\n', e, '\nExiting now.')
        exit(-1)

    return extract


def populateExtract(extract, useSpatial):
    try:
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
            if useSpatial:
                row.setSpatial(8, "POINT (30 10)")  # Destination
            table.insert(row)

    except TableauException as e:
        print('A fatal error occurred while populating the extract:\n', e, '\nExiting now.')
        exit(-1)



if __name__ == '__main__':
    ExtractAPI.initialize()
    filename = 'test_out.tde'
    # Create or Expand the Extract
    extract = createOrOpenExtract(filename, True)
    populateExtract(extract, True)

    # Flush the Extract to Disk
    extract.close()

    # Close the Tableau Extract API
    ExtractAPI.cleanup()

