
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


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####
####          DATABASE SETTINGS FOR "deepWebCrawlerPlugin".
####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
createTableCrawlerPluginPageServerDB="create table if not exists CrawlerPluginPage (id serial primary key, title varchar, page varchar NOT NULL, pageParent integer, body varchar NOT NULL, headers varchar NOT NULL, FOREIGN KEY (pageParent) REFERENCES CrawlerPluginPage(id) )"
createTableCrawlerPluginImageServerDB="create table if not exists CrawlerPluginImage (id serial primary key , imageSrc varchar)"
createTableCrawlerPluginPageImageServerDB="create table if not exists CrawlerPluginPageImage (page integer, image integer, FOREIGN KEY (page) REFERENCES CrawlerPluginPage(id), FOREIGN KEY (image) REFERENCES CrawlerPluginImage(id) )"
createTableCrawlerPluginFormServerDB="create table if not exists CrawlerPluginForm (id serial primary key , formName varchar, page integer, FOREIGN KEY (page) REFERENCES CrawlerPluginPage(id))"
createTableCrawlerPluginFormControlServerDB="create table if not exists CrawlerPluginFormControl (id serial primary key , form integer, controlName varchar, controlValue varchar, controlType varchar, FOREIGN KEY (form) REFERENCES CrawlerPluginForm(id))"
###     SELECTION
existsPageByUrlServerDB="select count(*) from CrawlerPluginPage where page = %s"
searchPageByUrlServerDB="select id from CrawlerPluginPage where page = %s"
existsImageByPageServerDB="select count(cppi.image) from CrawlerPluginImage cpi, CrawlerPluginPageImage cppi, CrawlerPluginPage cpp where cpi.id = cppi.image and cpp.id = cppi.page and cpi.imageSrc = %s and cpp.id = %s"
existsFormByPageServerDB="select count(cpf.page) from CrawlerPluginForm cpf where cpf.formName = %s and cpf.page = %s"

####    DML operations.
insertCrawlerPluginPageServerDB="insert into CrawlerPluginPage(title, page, pageParent, body, headers) values(%s,%s,%s,%s,%s) RETURNING id"
insertCrawlerPluginImageServerDB = "insert into CrawlerPluginImage(imageSrc) values(%s) RETURNING id"
insertCrawlerPluginPageImageServerDB = "insert into CrawlerPluginPageImage(page, image) values(%s,%s) RETURNING id"
insertCrawlerPluginPageFormServerDB = "insert into CrawlerPluginForm (formName, page) values(%s,%s) RETURNING id"
insertCrawlerPluginPageFormControlServerDB = "insert into CrawlerPluginFormControl (form, controlName, controlValue, controlType) values(%s,%s,%s,%s) RETURNING id"
truncateCrawlerPluginPageServerDB="delete from CrawlerPluginPage"
truncateCrawlerPluginPageImageServerDB="delete from CrawlerPluginPageImage"
truncateCrawlerPluginImageServerDB="delete from CrawlerPluginImage"
truncateCrawlerPluginFormServerDB="delete from CrawlerPluginForm"
truncateCrawlerPluginFormControlServerDB="delete from CrawlerPluginFormControl"
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
