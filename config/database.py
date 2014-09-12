################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE SETTINGS FOR SQLITE                                                                                                  ####
####                                                                                                                                        ####
####          CORE FUNCTIONALITIES                                                                                                          ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

databaseName="db/tortazo.db"
createTableScan="create table if not exists Scan (id integer primary key autoincrement, scanDate DATETIME not null, numNodes integer)"
createTableTorNodeData="create table if not exists TorNodeData (id integer primary key autoincrement, host varchar, state varchar, reason varchar, nickName varchar, fingerprint varchar, torVersion varchar, contact varchar, scanId integer, FOREIGN KEY (scanId) REFERENCES Scan(scanId))"
createTableTorNodePort="create table if not exists TorNodePort (id integer primary key autoincrement, state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer, FOREIGN KEY (torNodeId) REFERENCES TorNodeData(torNodeId))"
createTableOnionRepositoryProgress="create table if not exists OnionRepositoryProgress (id integer primary key autoincrement, partialOnionAddress VARCHAR(16) NOT NULL, validChars VARCHAR, startDate DATETIME not null, endDate DATETIME, progressFirstQuartet INTEGER, progressSecondQuartet INTEGER, progressThirdQuartet INTEGER, progressFourthQuartet INTEGER, UNIQUE(partialOnionAddress,validChars) )"
createTableOnionRepositoryResponses="create table if not exists OnionRepositoryResponses (id integer primary key autoincrement, onionAddress VARCHAR NOT NULL, responseCode VARCHAR, responseHeaders VARCHAR, onionDescription VARCHAR, serviceType VARCHAR NOT NULL, UNIQUE(onionAddress))"

####    Selects
selectTorNodeData="SELECT id, host, state, reason, nickName FROM TorNodeData WHERE scanId = ?"
selectTorNodePort="SELECT id, state, reason, port, name, version, torNodeId  FROM TorNodePort WHERE torNodeId = ?"
checkTorNodeData="SELECT count(*) FROM TorNodeData WHERE host = ? and nickName = ?"
selectTorScan="select id, scanDate from Scan limit ?"
selectTorScanIdentifier="select id, scanDate from Scan where id = ?"
nextIdHostNodeData="select max(node.id) from TorNodeData as node"
selectOnionRepositoryProgress="select id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet from OnionRepositoryProgress WHERE endDate IS NULL AND partialOnionAddress = ? AND validChars = ?"
selectOnionRepositoryResponses="select onionAddress, responseCode, responseHeaders,onionDescription, serviceType from OnionRepositoryResponses LIMIT ? OFFSET ? "
countOnionRepositoryResponses="select count(*) from OnionRepositoryResponses "

####    DML operations.
insertTorNodeData="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, scanId) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(scanDate, numNodes) values (%s, %s)"
insertOnionRepositoryProgress="insert into OnionRepositoryProgress(partialOnionAddress, validChars, startDate, endDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertOnionRepositoryResponses="insert into OnionRepositoryResponses(onionAddress, responseCode, responseHeaders,onionDescription, serviceType) values(?,?,?,?,?)"
updateOnionRepositoryProgress="update OnionRepositoryProgress set endDate =?,progressFirstQuartet=?,progressSecondQuartet=?,progressThirdQuartet=?,progressFourthQuartet=?  WHERE id=?"


truncateTorNodeData="delete from TorNodeData"
truncateTorNodePort="delete from TorNodePort"
truncateTorScan="delete from Scan"
truncateOnionRepositoryProgress="delete from OnionRepositoryProgress"
truncateOnionRepositoryResponses="delete from OnionRepositoryResponses"


####    Drop tables.
dropTableTorNodeData="drop table if exists TorNodeData"
dropTableTorNodePort="drop table if exists TorNodePort"
dropTableScan="drop table if exists Scan"
dropTableOnionRepositoryProgress="drop table if exists OnionRepositoryProgress"
dropTableOnionRepositoryResponses="drop table if exists OnionRepositoryResponses"


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE SETTINGS FOR SERVERDB - POSTGRESQL                                                                                   ####
####                                                                                                                                        ####
####          CORE FUNCTIONALITIES                                                                                                          ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
createTableScanServerDB="create table if not exists Scan (id serial primary key , scanDate DATE not null, numNodes integer)"
createTableTorNodeDataServerDB="create table if not exists TorNodeData (id serial primary key , host varchar, state varchar, reason varchar, nickName varchar, fingerprint varchar, torVersion varchar, contact varchar, scanId integer, FOREIGN KEY (scanId) REFERENCES Scan(id))"
createTableTorNodePortServerDB="create table if not exists TorNodePort (id serial primary key , state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer, FOREIGN KEY (torNodeId) REFERENCES TorNodeData(id))"
createTableOnionRepositoryProgressServerDB="create table if not exists OnionRepositoryProgress (id serial primary key , partialOnionAddress VARCHAR(16) NOT NULL, validChars VARCHAR, startDate DATE not null, endDate DATE, progressFirstQuartet INTEGER, progressSecondQuartet INTEGER, progressThirdQuartet INTEGER, progressFourthQuartet INTEGER, UNIQUE(partialOnionAddress,validChars) )"
createTableOnionRepositoryResponsesServerDB="create table if not exists OnionRepositoryResponses (id serial primary key , onionAddress VARCHAR NOT NULL, responseCode VARCHAR, responseHeaders VARCHAR, onionDescription VARCHAR, serviceType VARCHAR NOT NULL, UNIQUE(onionAddress))"

####    Selects
selectTorNodeDataServerDB="SELECT id, host, state, reason, nickName FROM TorNodeData WHERE scanId = %s"
selectTorNodePortServerDB="SELECT id, state, reason, port, name, version, torNodeId  FROM TorNodePort WHERE torNodeId = %s"
checkTorNodeDataServerDB="SELECT count(*) FROM TorNodeData WHERE host = %s and nickName = %s"
selectTorScanServerDB="select id, scanDate from Scan limit %s"
selectTorScanIdentifierServerDB="select id, scanDate from Scan where id = %s"
nextIdHostNodeDataServerDB="select max(node.id) from TorNodeData as node"
selectOnionRepositoryProgressServerDB="select id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet from OnionRepositoryProgress WHERE endDate IS NULL AND partialOnionAddress = %s AND validChars = %s"
selectOnionRepositoryResponsesServerDB="select onionAddress, responseCode, responseHeaders,onionDescription, serviceType from OnionRepositoryResponses LIMIT %s OFFSET %s "
countOnionRepositoryResponsesServerDB="select count(*) from OnionRepositoryResponses "

####    DML operations.
insertTorNodeDataServerDB="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, scanId) values(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
insertTorNodePortServerDB="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(%s, %s, %s, %s, %s, %s) RETURNING id"
insertTorScanServerDB="insert into Scan(scanDate, numNodes) values (%s, %s) RETURNING id"
insertOnionRepositoryProgressServerDB="insert into OnionRepositoryProgress(partialOnionAddress, validChars, startDate, endDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet) values(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
insertOnionRepositoryResponsesServerDB="insert into OnionRepositoryResponses(onionAddress, responseCode, responseHeaders,onionDescription, serviceType) values(%s,%s,%s,%s,%s) RETURNING id"
updateOnionRepositoryProgressServerDB="update OnionRepositoryProgress set endDate =%s,progressFirstQuartet=%s,progressSecondQuartet=%s,progressThirdQuartet=%s,progressFourthQuartet=%s  WHERE id=%s"


truncateTorNodeDataServerDB="delete from TorNodeData"
truncateTorNodePortServerDB="delete from TorNodePort"
truncateTorScanServerDB="delete from Scan"
truncateOnionRepositoryProgressServerDB="delete from OnionRepositoryProgress"
truncateOnionRepositoryResponsesServerDB="delete from OnionRepositoryResponses"


####    Drop tables.
dropTableTorNodeDataServerDB="drop table if exists TorNodeData"
dropTableTorNodePortServerDB="drop table if exists TorNodePort"
dropTableScanServerDB="drop table if exists Scan"
dropTableOnionRepositoryProgressServerDB="drop table if exists OnionRepositoryProgress"
dropTableOnionRepositoryResponsesServerDB="drop table if exists OnionRepositoryResponses"
