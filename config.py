####
####          REPORTING SETTINGS
####
ShodanOutputFile="/home/adastra/Escritorio/shodanReport.html"
NmapOutputFile="/home/adastra/Escritorio/nmapReport.html"

####
####          DATABASE SETTINGS
####

####    Creation of tables.
databaseName="tortazo.db"
createTableTorNodeData="create table if not exists TorNodeData (id integer primary key autoincrement, host varchar, state varchar, reason varchar, nickName varchar, scanId integer)"
createTableTorNodePort="create table if not exists TorNodePort (id integer primary key autoincrement, state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer)"
createTableScan="create table if not exists Scan (id integer primary key autoincrement, scanDate DATETIME not null, numNodes integer)"

####    Selection of hosts, ports and scans.
selectTorNodeData="SELECT id, host, state, reason, nickName FROM TorNodeData WHERE scanId = ?"
selectTorNodePort="SELECT id, state, reason, port, name, version, torNodeId  FROM TorNodePort WHERE torNodeId = ?"
selectTorScan="select id, scanDate from Scan limit ?"
lastAutoIncrement="select last_insert_rowid();"

####    DML operations.
insertTorNodeData="insert into TorNodeData(host, state, reason, nickName, scanId) values(?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(scanDate, numNodes) values(?,?)"
truncateTorNodeData="delete from TorNodeData"
truncateTorNodePort="delete from TorNodePort"
truncateTorScan="delete from Scan"


####    Drop tables.
dropTableTorNodeData="drop table if exists TorNodeData"
dropTableTorNodePort="drop table if exists TorNodePort"
dropTableScan="drop table if exists Scan"

####
####          NESUS SETTINGS
####
nessusHost="127.0.0.1"
nessusPort=8834
nessusUser="adastra"
nessusPass="peraspera"
nessusInitialSeq=200