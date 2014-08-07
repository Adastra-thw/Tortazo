################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE SETTINGS                                                                                                             ####
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
createTableOnionRepositoryResponses="create table if not exists OnionRepositoryResponses (id integer primary key autoincrement, onionAddress VARCHAR NOT NULL, responseCode VARCHAR, responseHeaders VARCHAR, onionDescription VARCHAR, UNIQUE(onionAddress))"

####    Selects
selectTorNodeData="SELECT id, host, state, reason, nickName FROM TorNodeData WHERE scanId = ?"
selectTorNodePort="SELECT id, state, reason, port, name, version, torNodeId  FROM TorNodePort WHERE torNodeId = ?"
checkTorNodeData="SELECT count(*) FROM TorNodeData WHERE host = ? and nickName = ?"
selectTorScan="select id, scanDate from Scan limit ?"
selectTorScanIdentifier="select id, scanDate from Scan where id = ?"
nextIdHostNodeData="select max(node.id) from TorNodeData as node"
selectOnionRepositoryProgress="select id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet from OnionRepositoryProgress WHERE endDate IS NULL AND partialOnionAddress = ? AND validChars = ?"

####    DML operations.
insertTorNodeData="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, scanId) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(scanDate, numNodes) values(?,?)"
insertOnionRepositoryProgress="insert into OnionRepositoryProgress(partialOnionAddress, validChars, startDate, endDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertOnionRepositoryResponses="insert into OnionRepositoryResponses(onionAddress, responseCode, responseHeaders,onionDescription) values(?,?,?,?)"
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
