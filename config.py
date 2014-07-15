from os.path import expanduser
home = expanduser("~")
####
####          REPORTING SETTINGS
####
ShodanOutputFile=home+"/shodanReport.html"
NmapOutputFile=home+"/nmapReport.html"
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####
####          DATABASE SETTINGS
####
####    Creation of tables.
databaseName="db/tortazo.db"
createTableTorNodeData="create table if not exists TorNodeData (id integer primary key autoincrement, host varchar, state varchar, reason varchar, nickName varchar, fingerprint varchar, torVersion varchar, contact varchar, scanId integer)"
createTableTorNodePort="create table if not exists TorNodePort (id integer primary key autoincrement, state varchar, reason varchar, port integer, name varchar, version varchar, torNodeId integer)"
createTableScan="create table if not exists Scan (id integer primary key autoincrement, scanDate DATETIME not null, numNodes integer)"

####    Selection of hosts, ports and scans.
selectTorNodeData="SELECT id, host, state, reason, nickName FROM TorNodeData WHERE scanId = ?"
selectTorNodePort="SELECT id, state, reason, port, name, version, torNodeId  FROM TorNodePort WHERE torNodeId = ?"
checkTorNodeData="SELECT count(*) FROM TorNodeData WHERE host = ? and nickName = ?"
selectTorScan="select id, scanDate from Scan limit ?"
selectTorScanIdentifier="select id, scanDate from Scan where id = ?"
nextIdHostNodeData="select max(node.id) from TorNodeData as node"
####    DML operations.
insertTorNodeData="insert into TorNodeData(host, state, reason, nickName, fingerprint, torVersion, contact, scanId) values(?, ?, ?, ?, ?, ?, ?, ?)"
insertTorNodePort="insert into TorNodePort(state, reason, port, name, version, torNodeId) values(?, ?, ?, ?, ?, ?)"
insertTorScan="insert into Scan(scanDate, numNodes) values(?,?)"
truncateTorNodeData="delete from TorNodeData"
truncateTorNodePort="delete from TorNodePort"
truncateTorScan="delete from Scan"
####    Drop tables.
dropTableTorNodeData="drop table if exists TorNodeData"
dropTableTorNodePort="drop table if exists TorNodePort"
dropTableScan="drop table if exists Scan"

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####
####          DATABASE SETTINGS FOR "deepWebCrawlerPlugin".
####
createTableCrawlerPluginLinks="create table if not exists CrawlerPluginLinks (id integer primary key autoincrement, link varchar, linkParent integer, FOREIGN KEY (linkParent) REFERENCES CrawlerPluginLinks(id) )"
createTableCrawlerPluginImages="create table if not exists CrawlerPluginImages (id integer primary key autoincrement, link integer, imageSrc, FOREIGN KEY (link) REFERENCES CrawlerPluginLinks(id) )"
createTableCrawlerPluginFormData="create table if not exists CrawlerPluginFormData (id integer primary key autoincrement, link integer, formAttributeName varchar, formAttributeValue varchar, formAttributeType varchar, FOREIGN KEY (link) REFERENCES  CrawlerPluginLinks(id) )"
####    DML operations.
insertCrawlerPluginLinks="insert into CrawlerPluginLinks(id, link, linkParent) values(?,?,?)"
insertCrawlerPluginImages="insert into CrawlerPluginImages(id, link, imageSrc) values(?,?,?)"
insertCrawlerPluginFormData="insert into CrawlerPluginFormData(id, link, formAttributeName, formAttributeValue, formAttributeType) values(?,?,?,?,?)"

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####
####          NESSUS SETTINGS
####
nessusHost="127.0.0.1"
nessusPort=8834
nessusUser="adastra"
nessusPass="adastra"
nessusInitialSeq=200
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####
####          SOCKS SETTINGS
####
socksHost="127.0.0.1"
#Default Socks Port if TOR has been started with tor-browser.
# If you start manually TOR using the command "tor -f torrc" the default Socks Port will be 9050. Beware with that!!
socksPort=9150
timeOutRequests=15