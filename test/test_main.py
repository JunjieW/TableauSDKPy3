# ------------------------------------------------------------------------------
#
#   This file is the copyrighted property of Tableau Software and is protected
#   by registered patents and other applicable U.S. and international laws and
#   regulations.
#
#   Unlicensed use of the contents of this file is prohibited. Please refer to
#   the NOTICES.txt file for further details.
#
# ------------------------------------------------------------------------------

import argparse
import sys
import textwrap

from tableausdk import *
from tableausdk.Extract import *
from tableausdk.Server import *


# ------------------------------------------------------------------------------
#   Parse Arguments
# ------------------------------------------------------------------------------
def parseArguments():
    parser = argparse.ArgumentParser(description='A simple demonstration of the Tableau SDK.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    # (NOTE: '-h' and '--help' are defined by default in ArgumentParser
    parser.add_argument('-b', '--build', action='store_true',  # default=False,
                        help=textwrap.dedent('''\
                            If an extract named FILENAME exists, open it and add data to
                            it. If no such extract exists, create one and add data to it.
                            If no FILENAME is specified, the default is used.
                            (default=%(default)s)

                            '''))
    parser.add_argument('-s', '--spatial', action='store_true',  # default=False,
                        help=textwrap.dedent('''\
                            If creating a new extract, include spatial data when adding
                            data. If '--build' is not specified, or the extract being
                            built is not newly created, this argument is ignored.
                            (default=%(default)s)

                            '''))
    parser.add_argument('-p', '--publish', action='store_true',  # default=False,
                        help=textwrap.dedent('''\
                            Publish an extract named FILENAME to a Tableau Server instance
                            running at HOSTNAME, creating a published datasource named
                            DATASOURCE_NAME on the server under the PROJECT_NAME project.

                            If '--overwrite' is specified, if there is an existing
                            published datasource on the server named DATASOURCE_NAME under
                            the PROJECT_NAME project, it is overwritten.
                            USERNAME, PASSWORD, and SITEID are used to connect to the
                            server.

                            If any of '--filename', '--project-name', '--datasource-name',
                            '--overwrite', '--hostname', '--username', '--password',
                            or '--site-id' are not specified, the corresponding default
                            value(s) are used.

                            (NOTE: If '--username', '--password', and '--site-id' are not
                             each specified, '--publish' will not succeed.)
                            (default=%(default)s)

                            '''))
    parser.add_argument('-o', '--overwrite', action='store_true',  # default=False,
                        help=textwrap.dedent('''\
                            Overwrite any existing published datasource named
                            DATASOURCE_NAME under the PROJECT_NAME project on the server.
                            If '--project-name' and/or '--datasource-name' are not
                            specified, the corresponding default value(s) are used. If
                            '--publish' is not specified, this argument is ignored
                            (default=%(default)s)

                            '''))
    parser.add_argument('-f', '--filename', action='store', metavar='FILENAME', default='order-py.tde',
                        help=textwrap.dedent('''\
                            Use FILENAME as the extract filename when creating, opening,
                            and/or publishing an extract. If neither '--build' nor
                            '--publish' is specified, this argument is ignored.
                            (default='%(default)s')

                            '''))
    parser.add_argument('--project-name', action='store', metavar='PROJECT_NAME', default='default',
                        help=textwrap.dedent('''\
                            Use PROJECT_NAME as the project-name when creating publishing
                            an extract. If '--publish' is not specified, this argument is
                            ignored.
                            (default='%(default)s')

                            '''))
    parser.add_argument('--datasource-name', action='store', metavar='DATASOURCE_NAME', default='order-py',
                        help=textwrap.dedent('''\
                            Use DATASOURCE_NAME as the datasource name when creating
                            publishing an extract. If '--publish' is not specified, this
                            argument is ignored.
                            (default='%(default)s')

                            '''))
    parser.add_argument('--hostname', action='store', metavar='HOSTNAME', default='http://localhost',
                        help=textwrap.dedent('''\
                            Connect to a Tableau Server instance running at HOSTNAME to
                            publish an extract. If '--publish' is not specified, this
                            argument is ignored.
                            (default='%(default)s')

                            '''))
    parser.add_argument('--username', action='store', metavar='USERNAME', default='username',
                        help=textwrap.dedent('''\
                            Connect to the server as user USERNAME to publish an extract.
                            If '--publish' is not specified, this argument is ignored.

                            (NOTE: This argument must be specified for '--publish' to
                             succeed. Admin privileges are required in Tableau Server to
                             publish datasources using the Tableau SDK Server API.)
                            (default='%(default)s')

                            '''))
    parser.add_argument('--password', action='store', metavar='PASSWORD', default='password',
                        help=textwrap.dedent('''\
                            Connect to the server using password PASSWORD to publish an
                            extract. If '--publish' is not specified, this argument is
                            ignored.

                            (NOTE: This argument must be specified for '--publish' to
                             succeed. Admin privileges are required in Tableau Server to
                             publish datasources using the Tableau SDK Server API.)
                            (default='%(default)s')

                            '''))
    parser.add_argument('--site-id', action='store', metavar='SITEID', default='siteID',
                        help=textwrap.dedent('''\
                            Connect to the server using siteID SITEID to publish an
                            extract. If '--publish' is not specified, this argument is
                            ignored.

                            (NOTE: This argument must be specified for '--publish' to
                             succeed. Admin privileges are required in Tableau Server to
                             publish datasources using the Tableau SDK Server API.)
                            (default='%(default)s')

                            '''))
    return vars(parser.parse_args())


# ------------------------------------------------------------------------------
#   Create Extract
# ------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def createOrOpenExtract(
        filename,
        useSpatial
):
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
                print
                'A fatal error occurred while creating the table:\nExiting now\n.'
                exit(-1)

    except TableauException, e:
        print
        'A fatal error occurred while creating the new extract:\n', e, '\nExiting now.'
        exit(-1)

    return extract


# ------------------------------------------------------------------------------
#   Populate Extract
# ------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def populateExtract(
        extract,
        useSpatial
):
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

    except TableauException, e:
        print
        'A fatal error occurred while populating the extract:\n', e, '\nExiting now.'
        exit(-1)


# ------------------------------------------------------------------------------
#   Publish Extract
# ------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Server API is initialized)
def publishExtract(
        filename,
        projectName,
        datasourceName,
        overwrite,
        hostname,
        username,
        password,
        siteID
):
    try:
        # Create the Server Connection Object
        serverConnection = ServerConnection()

        # Connect to the Server
        serverConnection.connect(hostname, username, password, siteID)

        # Publish the Extract to the Server
        serverConnection.publishExtract(filename, projectName, datasourceName, overwrite)

        # Disconnect from the Server
        serverConnection.disconnect()

        # Destroy the Server Connection Object
        serverConnection.close()

    except TableauException, e:
        errorMessage = 'A fatal error occurred while publishing the extract:\n'
        if e.errorCode == Result.INTERNAL_ERROR:
            errorMessage += 'INTERNAL_ERROR - Could not parse the response from the server.'
        elif e.errorCode == Result.INVALID_ARGUMENT:
            errorMessage += 'INVALID_ARGUMENT - ' + e.message
        elif e.errorCode == Result.CURL_ERROR:
            errorMessage += 'CURL_ERROR - ' + e.message
        elif e.errorCode == Result.SERVER_ERROR:
            errorMessage += 'SERVER_ERROR - ' + e.message
        elif e.errorCode == Result.NOT_AUTHENTICATED:
            errorMessage += 'NOT_AUTHENTICATED - ' + e.message
        elif e.errorCode == Result.BAD_PAYLOAD:
            errorMessage += 'BAD_PAYLOAD - Unknown response from the server. Make sure this version of Tableau API is compatible with your server.'
        elif e.errorCode == Result.INIT_ERROR:
            errorMessage += 'INIT_ERROR - ' + e.message
        else:
            errorMessage += 'An unknown error occured.'
        print
        errorMessage, '\nExiting now.'
        exit(-1)


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------
def main():
    # Parse Arguments
    options = parseArguments()

    # Extract API Demo
    if (options['build']):
        # Initialize the Tableau Extract API
        ExtractAPI.initialize()

        # Create or Expand the Extract
        extract = createOrOpenExtract(options['filename'], options['spatial'])
        populateExtract(extract, options['spatial'])

        # Flush the Extract to Disk
        extract.close()

        # Close the Tableau Extract API
        ExtractAPI.cleanup()

    # Server API Demo
    if (options['publish']):
        # Initialize Tableau Server API
        ServerAPI.initialize()

        # Publish the Extract
        publishExtract(options['filename'], options['project_name'], options['datasource_name'], options['overwrite'],
                       options['hostname'], options['username'], options['password'], options['site_id'])

        # Clean up Tableau Server API
        ServerAPI.cleanup()

    return 0


if __name__ == "__main__":
    retval = main()
    sys.exit(retval)
