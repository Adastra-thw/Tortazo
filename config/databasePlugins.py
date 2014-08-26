################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####
####          DATABASE SETTINGS FOR "deepWebCrawlerPlugin".
####
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
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
