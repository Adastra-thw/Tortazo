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
createTableTorNodeData="create table if not exists TorNodeData (id integer primary key autoincrement, host varchar, state varchar, reason varchar, nickName varchar, fingerprint varchar, torVersion varchar, contact varchar, scanId integer)"
createTableTorNodePort="create table if not exists TorNodePort (id integer primary key autoincrement, state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer)"
createTableScan="create table if not exists Scan (id integer primary key autoincrement, scanDate DATETIME not null, numNodes integer)"
createTableOnionRepositoryProgress="create table if not exists OnionRepositoryProgress (id integer primary key autoincrement, partialOnionAddress VARCHAR(16) NOT NULL, startDate DATETIME not null, endDate DATETIME not null, progressFirstQuartet INTEGER, progressSecondQuartet INTEGER, progressThirdQuartet INTEGER, progressFourthQuartet INTEGER, UNIQUE(partialOnionAddress) )"
createTableOnionRepositoryResponses="create table if not exists OnionRepositoryResponses (id integer primary key autoincrement, onionAddress VARCHAR NOT NULL, responseCode VARCHAR, responseHeaders VARCHAR)"

####    Selects
selectTorNodeData="SELECT id, host, state, reason, nickName FROM TorNodeData WHERE scanId = ?"
selectTorNodePort="SELECT id, state, reason, port, name, version, torNodeId  FROM TorNodePort WHERE torNodeId = ?"
checkTorNodeData="SELECT count(*) FROM TorNodeData WHERE host = ? and nickName = ?"
selectTorScan="select id, scanDate from Scan limit ?"
selectTorScanIdentifier="select id, scanDate from Scan where id = ?"
nextIdHostNodeData="select max(node.id) from TorNodeData as node"
selectOnionRepositoryProgress="select id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet from OnionRepositoryProgress WHERE endDate IS NULL AND partialOnionAddress = ?"

####    DML operations.
insertTorNodeData="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, scanId) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(scanDate, numNodes) values(?,?)"
insertOnionRepositoryProgress="insert into OnionRepositoryProgress(partialOnionAddress, startDate, endDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet) values(?, ?, ?, ?, ?, ?, ?)"
insertOnionRepositoryResponses="insert into OnionRepositoryResponses(onionAddress, responseCode, responseHeaders) values(?,?,?)"
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
####          DATABASE SETTINGS FOR "deepWebCrawlerPlugin".                                                                                 ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

createTableCrawlerPluginPage="create table if not exists CrawlerPluginPage (id integer primary key autoincrement, title varchar, page varchar NOT NULL, pageParent integer, body varchar NOT NULL, headers varchar NOT NULL, FOREIGN KEY (pageParent) REFERENCES CrawlerPluginPage(id) )"
createTableCrawlerPluginPageImage="create table if not exists CrawlerPluginPageImage (page integer, image integer, FOREIGN KEY (page) REFERENCES CrawlerPluginPage(page), FOREIGN KEY (image) REFERENCES CrawlerPluginImage(image) )"
createTableCrawlerPluginImage="create table if not exists CrawlerPluginImage (id integer primary key autoincrement, imageSrc varchar)"
createTableCrawlerPluginForm="create table if not exists CrawlerPluginForm (id integer primary key autoincrement, formName varchar, page integer, FOREIGN KEY (page) REFERENCES CrawlerPluginPage(page))"
createTableCrawlerPluginFormControl="create table if not exists CrawlerPluginFormControl (id integer primary key autoincrement, form integer, controlName varchar, controlValue varchar, controlType varchar, FOREIGN KEY (form) REFERENCES CrawlerPluginForm(page))"
###     SELECTION
existsPageByUrl="select count(*) from CrawlerPluginPage where page = ?"
searchPageByUrl="select id from CrawlerPluginPage where page = ?"
existsImageByPage="select count(cppi.image) from CrawlerPluginImage cpi, CrawlerPluginPageImage cppi, CrawlerPluginPage cpp where cpi.id = cppi.image and cpp.id = cppi.page and cpi.imageSrc = ? and cpp.id = ?"
existsFormByPage="select count(cpf.page) from CrawlerPluginForm cpf where cpf.formName = ? and cpf.page = ?"

####    DML operations.
insertCrawlerPluginPage="insert into CrawlerPluginPage(title, page, pageParent, body, headers) values(?,?,?,?,?)"
insertCrawlerPluginImage = "insert into CrawlerPluginImage(imageSrc) values(?)"
insertCrawlerPluginPageImage = "insert into CrawlerPluginPageImage(page, image) values(?,?)"
insertCrawlerPluginPageForm = "insert into CrawlerPluginForm (formName, page) values(?,?)"
insertCrawlerPluginPageFormControl = "insert into CrawlerPluginFormControl (form, controlName, controlValue, controlType) values(?,?,?,?)"
truncateCrawlerPluginPage="delete from CrawlerPluginPage"
truncateCrawlerPluginPageImage="delete from CrawlerPluginPageImage"
truncateCrawlerPluginImage="delete from CrawlerPluginImage"
truncateCrawlerPluginForm="delete from CrawlerPluginForm"
truncateCrawlerPluginFormControl="delete from CrawlerPluginFormControl"
