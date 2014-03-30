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
createTableTorNodeData="create table if not exists TorNodeData (id integer primary key, host varchar, state varchar, reason varchar, nickName varchar)"
createTableTorNodePort="create table if not exists TorNodePort (id integer primary key, state varchar, reason varchar, port integer, name varchar, version varchar, torNode integer NOT NULL)"
createTableScan="create table if not exists Scan (id integer primary key autoincrement, nodeId integer not null, portId integer not null, scanDate DATETIME not null)"
createTableNodeHistory="create table if not exists TorNodeDataHistory (id integer primary key autoincrement, torNodeId integer, host varchar, state varchar, reason varchar, nickName varchar)"
createTablePortHistory="create table if not exists TorNodePortHistory (id integer primary key autoincrement, state varchar, reason varchar, port integer, name varchar, version varchar, torNode integer NOT NULL)"

####    Selection of hosts, ports and scans.
selectTorNodeData="SELECT id, host, state, reason, nickName FROM TorNodeData"
selectTorNodePort="SELECT id, state, reason, port, name, version, torNode FROM TorNodePort WHERE torNode = ?"
selectTorScan="select nodeId, portId from Scan"
lastAutoIncrement="select last_insert_rowid();"

####    DML operations.
insertTorNodeData="insert into TorNodeData(id, host, state, reason, nickName) values(?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(id, state, reason, port, name, version, torNode) values(?, ?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(nodeId, portId, scanDate) values(?, ?, ?)"
insertTorNodeDataHistory="insert into TorNodeDataHistory (torNodeId, host, state, reason, nickName) select id, host, state, reason, nickName from TorNodeData "
insertTorNodePortHistory="insert into TorNodePortHistory (state, reason, port, name, version, torNode) select state, reason, port, name, version, torNode from TorNodePort"
updateTorScan="update Scan set nodeId = ?, portId =?, scanDate = ?"
truncateTorNodeData="delete from TorNodeData"
truncateTorNodePort="delete from TorNodePort"

####    Drop tables.
dropTableTorNodeData="drop table if exists TorNodeData"
dropTableTorNodePort="drop table if exists TorNodePort"

####
####          NESUS SETTINGS
####
nessusHost="127.0.0.1"
nessusPort=8834
nessusUser="adastra"
nessusPass="peraspera"
nessusInitialSeq=200
