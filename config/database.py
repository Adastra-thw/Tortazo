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
createTableScan="create table if not exists Scan (id integer primary key autoincrement, scanDate DATETIME not null, numNodes integer, tortazoCommand varchar, scanFinished varchar(2))" #scanFinished = 1: Finished; scanFinished = 0: Pending
createTableTorNodeData="create table if not exists TorNodeData (id integer primary key autoincrement, host varchar, state varchar, reason varchar, nickName varchar, fingerprint varchar, torVersion varchar, contact varchar, scanId integer, operative_system varchar, FOREIGN KEY (scanId) REFERENCES Scan(scanId))"
createTableTorNodePort="create table if not exists TorNodePort (id integer primary key autoincrement, state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer, FOREIGN KEY (torNodeId) REFERENCES TorNodeData(torNodeId))"
createTableOnionRepositoryProgress="create table if not exists OnionRepositoryProgress (id integer primary key autoincrement, partialOnionAddress VARCHAR(16) NOT NULL, validChars VARCHAR, startDate DATETIME not null, endDate DATETIME, progressFirstQuartet INTEGER, progressSecondQuartet INTEGER, progressThirdQuartet INTEGER, progressFourthQuartet INTEGER, UNIQUE(partialOnionAddress,validChars) )"
createTableOnionRepositoryResponses="create table if not exists OnionRepositoryResponses (id integer primary key autoincrement, onionAddress VARCHAR NOT NULL, responseCode VARCHAR, responseHeaders VARCHAR, onionDescription VARCHAR, serviceType VARCHAR NOT NULL, UNIQUE(onionAddress))"

createTableBotnetNode="create table if not exists BotnetNode (id integer primary key autoincrement, address VARCHAR NOT NULL, userservice VARCHAR, password VARCHAR, port integer, nickname VARCHAR, serviceType VARCHAR)"
createTableBotnetGeolocation="create table if not exists BotnetGeolocation (id integer primary key autoincrement, botnetNodeId integer, botLatitute REAL, botLongitute REAL, FOREIGN KEY (botnetNodeId) REFERENCES BotnetNode(id))"
createTableTorNodeGeolocation="create table if not exists TorNodeGeolocation (id integer primary key autoincrement, torNodeId integer, nodeLatitute REAL, nodeLongitute REAL, FOREIGN KEY (torNodeId) REFERENCES TorNodeData(id))"


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
selectBotnetNode="select address, userservice, password, port, nickname, serviceType from BotnetNode where address = ?"
nextIdBotnetNode="select max(node.id) from BotnetNode as node"

####    DML operations.
insertTorNodeData="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, operative_system, scanId) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(scanDate, numNodes) values (?, ?)"
updateTorScan="update Scan set numNodes = ? where id = ?"
insertOnionRepositoryProgress="insert into OnionRepositoryProgress(partialOnionAddress, validChars, startDate, endDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertOnionRepositoryResponses="insert into OnionRepositoryResponses(onionAddress, responseCode, responseHeaders,onionDescription, serviceType) values(?,?,?,?,?)"
updateOnionRepositoryProgress="update OnionRepositoryProgress set endDate =?,progressFirstQuartet=?,progressSecondQuartet=?,progressThirdQuartet=?,progressFourthQuartet=?  WHERE id=?"
insertBotnetNode="insert into BotnetNode(address, userservice, password, port, nickname, serviceType) values(?, ?, ?, ?, ?, ?)"
insertBotnetGeolocation="insert into BotnetGeolocation(botnetNodeId, botLatitute, botLongitute) values(?, ?, ?)"
insertTorNodeGeolocation="insert into TorNodeGeolocation(torNodeId, nodeLatitute, nodeLongitute) values(?, ?, ?)"


truncateTableBotnetGeolocation="delete from BotnetGeolocation"
truncateTableTorNodeGeolocation="delete from TorNodeGeolocation"
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
dropTableBotnetNode="drop table if exists BotnetNode"
dropTableBotnetGeolocation="drop table if exists BotnetGeolocation"
dropTableTorNodeGeolocation="drop table if exists TorNodeGeolocation"


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
createTableScanServerDB="create table if not exists Scan (id serial primary key , scanDate DATE not null, numNodes integer, tortazoCommand varchar, scanFinished varchar(2))" #scanFinished = 1: Finished; scanFinished = 0: Pending
createTableTorNodeDataServerDB="create table if not exists TorNodeData (id serial primary key , host varchar, state varchar, reason varchar, nickName varchar, fingerprint varchar, torVersion varchar, contact varchar, scanId integer, operative_system varchar, FOREIGN KEY (scanId) REFERENCES Scan(id))"
createTableTorNodePortServerDB="create table if not exists TorNodePort (id serial primary key , state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer, FOREIGN KEY (torNodeId) REFERENCES TorNodeData(id))"
createTableOnionRepositoryProgressServerDB="create table if not exists OnionRepositoryProgress (id serial primary key , partialOnionAddress VARCHAR(16) NOT NULL, validChars VARCHAR, startDate DATE not null, endDate DATE, progressFirstQuartet INTEGER, progressSecondQuartet INTEGER, progressThirdQuartet INTEGER, progressFourthQuartet INTEGER, UNIQUE(partialOnionAddress,validChars) )"
createTableOnionRepositoryResponsesServerDB="create table if not exists OnionRepositoryResponses (id serial primary key , onionAddress VARCHAR NOT NULL, responseCode VARCHAR, responseHeaders VARCHAR, onionDescription VARCHAR, serviceType VARCHAR NOT NULL, UNIQUE(onionAddress))"
createTableBotnetNodeServerDB="create table if not exists BotnetNode (id serial primary key , address varchar not null, userservice varchar, password varchar, port integer, nickname varchar, serviceType varchar)"
createTableBotnetGeolocationServerDB="create table if not exists BotnetGeolocation (id serial primary key, botnetNodeId integer, botLatitute double precision, botLongitute double precision, FOREIGN KEY (botnetNodeId) REFERENCES BotnetNode(id))"
createTableTorNodeGeolocationServerDB="create table if not exists TorNodeGeolocation (id serial primary key, torNodeId integer, nodeLatitute double precision, nodeLongitute double precision, FOREIGN KEY (torNodeId) REFERENCES TorNodeData(id))"


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
selectBotnetNodeServerDB="select address, userservice, password, port, nickname, serviceType from BotnetNode where address = %s"
nextIdBotnetNodeServerDB="select max(bot.id) from BotnetNode as bot"


####    DML operations.
insertTorNodeDataServerDB="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, operative_system, scanId) values(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
insertTorNodePortServerDB="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(%s, %s, %s, %s, %s, %s) RETURNING id"
insertTorScanServerDB="insert into Scan(scanDate, numNodes) values (%s, %s) RETURNING id"
updateTorScanServerDB="update Scan set numNodes = %s where id = %s"
insertOnionRepositoryProgressServerDB="insert into OnionRepositoryProgress(partialOnionAddress, validChars, startDate, endDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet) values(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
insertOnionRepositoryResponsesServerDB="insert into OnionRepositoryResponses(onionAddress, responseCode, responseHeaders,onionDescription, serviceType) values(%s,%s,%s,%s,%s) RETURNING id"
updateOnionRepositoryProgressServerDB="update OnionRepositoryProgress set endDate =%s,progressFirstQuartet=%s,progressSecondQuartet=%s,progressThirdQuartet=%s,progressFourthQuartet=%s  WHERE id=%s"
insertBotnetNodeServerDB="insert into BotnetNode(address, userservice, password, port, nickname, serviceType) values(%s, %s, %s, %s, %s, %s) RETURNING id"
insertBotnetGeolocationServerDB="insert into BotnetGeolocation(botnetNodeId, botLatitute, botLongitute) values(%s, %s, %s) RETURNING id"
insertTorNodeGeolocationServerDB="insert into TorNodeGeolocation(torNodeId, nodeLatitute, nodeLongitute) values(%s, %s, %s) RETURNING id"


truncateTorNodeDataServerDB="delete from TorNodeData"
truncateTorNodePortServerDB="delete from TorNodePort"
truncateTorScanServerDB="delete from Scan"
truncateOnionRepositoryProgressServerDB="delete from OnionRepositoryProgress"
truncateOnionRepositoryResponsesServerDB="delete from OnionRepositoryResponses"
truncateBotnetNodeServerDB="delete from BotnetNode"
truncateBotnetGeolocationServerDB="delete from BotnetGeolocation"
truncateTorNodeGeolocationServerDB="delete from TorNodeGeolocation"


####    Drop tables.
dropTableTorNodeDataServerDB="drop table if exists TorNodeData"
dropTableTorNodePortServerDB="drop table if exists TorNodePort"
dropTableScanServerDB="drop table if exists Scan"
dropTableOnionRepositoryProgressServerDB="drop table if exists OnionRepositoryProgress"
dropTableOnionRepositoryResponsesServerDB="drop table if exists OnionRepositoryResponses"
dropTableBotnetNodeServerDB="drop table if exists BotnetNode"
dropTableBotnetGeolocationServerDB="drop table if exists BotnetGeolocation"
dropTableTorNodeGeolocationServerDB="drop table if exists TorNodeGeolocation"
