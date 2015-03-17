"""
Script for exploring interacting with databases using IronPython & .NET
"""
import clr
clr.AddReference('System.Data')
from System.Data.SqlClient import SqlConnection
from System.Data import CommandBehavior


# populate
info = None  # server, db tuple
table = None  # table name (include schema)

def build_connection_string(server, database, trusted=True):
    base = 'SERVER={0};DATABASE={1};Trusted_Connection={2}'
    trusted_con = 'no'
    if trusted:
        trusted_con = 'yes'
    return(base.format(server, database, trusted_con))

con = SqlConnection(build_connection_string(*info))

con.Open()

query = con.CreateCommand()
query.CommandText = 'SELECT TOP 10 * FROM ' + table
# CommandBehavior.SequentialAccess supposedly highly performant
reader = query.ExecuteReader(CommandBehavior.CloseConnection)

ncol = reader.FieldCount

# use python string formatting for printing results
base_format = list()
for i in xrange(ncol):
    base_format.append('{{{0}:<18}}'.format(i))  # double curly brackets to escape
base_format = ''.join(base_format)

print base_format.format(*[str(reader.GetName(i)) for i in xrange(ncol)])
while reader.Read():
    record = [str(reader[i]) for i in xrange(ncol)]
    print base_format.format(*record)
