# tableausdkpy3 and tableausdk2py3

- tableausdkpy3: python3.4+ support for Tableau SDK with .tde as extract file
  - https://onlinehelp.tableau.com/current/api/sdk/en-us/help.htm

- tableausdk2py3: python3.4+ support for Tableau SDK (API 2.0) with .hyper as extract file
  - https://onlinehelp.tableau.com/current/api/extract_api/en-us/help.htm


# For Developers

### setup
Run the `unzip_large_tableau_sdk_binary.sh` script (in git bash) to (or manually) unzip them to `tableausdk2py3/bin/hyper/`


  
# Limitation:
- Currently run only in Windows (but integration of linux and MacOS is possible)



# Requirements
- Python 3.x with x >= 4
- Pandas >= 0.19.2
- dateutil >= 2.5.2
- pyodbc >= 3.0.10




# Installation

### setup.py
*Step-1*
Make sure you have the hyper binary (`hyperd.exe` and `hyperd_sse2.exe`) unzip'ed in `tableausdk2py3/bin/hyper/`. 
If not, run the `unzip_large_tableau_sdk_binary.sh` script (in git bash) to (or manually) unzip them to `tableausdk2py3/bin/hyper/`

*Step-2*
In directory of this repo, run following command.

NOTE: Run as root on POSIX platforms

NOTE: clear the build folder, if it exists (should be at the same dir as the setup script named `build` by default), every time before you run the following commands

* tableausdkpy3 *
```bash
python setup_tableausdkpy3.py build
python setup_tableausdkpy3.py install
```

* tableausdk2py3 *
```bash
python setup_tableausdk2py3.py build
python setup_tableausdk2py3.py install
```

### PyPI
...

### Conda
...


# Get Started
## Setting environment variables for Log and Temp Files (Optional)

Optionally, you can set the following environment variables to specify working directories for the Extract API. If you don't set these variables, the Extract API uses the current working directory as the default location.

Note: The user identity under which code is running must have write permissions to the locations you specify in these environment variables.

`TAB_SDK_LOGDIR` The folder where the Extract API writes the DataExtract.log file.

`TAB_SDK_TMPDIR` The temporary directory where the Extract API keeps intermediate (temporary) files, such as when it's creating an extract.

see more at:
- [Tableau Hyper API Documentation](https://onlinehelp.tableau.com/current/api/extract_api/en-us/help.htm#Extract/extract_api_installing.htm%3FTocPath)
- [Tableau Extract API Documentation](https://onlinehelp.tableau.com/current/api/sdk/en-us/help.htm#SDK/tableau_sdk_installing.htm%3FTocPath)

## Sample Code
```python
import pyodbc
from tableausdk2py3 import *

############################################
# For TdeWriter:
#-------------------------------------------
# from tableausdkpy3 import *
############################################

OUTPUT = 'test.hyper'
server = 'rsk-db-uat'
db = 'Reporting'

# NOTE: Make sure to use ODBC Driver instead of "SQL Server", otherwise pyodbc will convert SQL datetime/date into str
conn_str = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=' + server + ';DATABASE=' + db + ';Trusted_Connection=yes'

conn = pyodbc.connect(conn_str , autocommit=True)
cursor = conn.cursor()
q = "SELECT TABLE_NAME FROM Reporting.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
cursor.execute(q)

hyper_writer = TableauHyperWriter(OUTPUT)
hyper_writer.write_from_pyodbc_cursor(cursor)

############################################
# For TdeWriter:
#-------------------------------------------
# tde_writer = TableauTdeWriter(OUTPUT)
# tde_writer.write_from_pyodbc_cursor(cursor)
############################################

# NOTE: It's the client/caller's responsibility to close the cursor and connection
cursor.close()
conn.close()
```




