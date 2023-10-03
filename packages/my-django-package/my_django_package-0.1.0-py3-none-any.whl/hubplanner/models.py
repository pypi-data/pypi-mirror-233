from django.db import models
# from models import Person, Project

# Create your models here.
# class Projectdetail_EstimatingDB(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     projectnumber = models.CharField(db_column='ProjectNumber', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     revisionnumber = models.IntegerField(db_column='RevisionNumber')  # Field name made lowercase.
#     baseversion = models.CharField(db_column='BaseVersion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     totalcost = models.DecimalField(db_column='TotalCost', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     totalsell = models.DecimalField(db_column='TotalSell', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     blendedmargin = models.DecimalField(db_column='BlendedMargin', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
#     modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
#     baseversiondescription = models.CharField(db_column='BaseVersionDescription', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     qouteid = models.IntegerField(db_column='QouteId')  # Field name made lowercase.
#     createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#     optionversion = models.CharField(db_column='OptionVersion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     optionversiondescription = models.CharField(db_column='OptionVersionDescription', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     customer = models.CharField(db_column='Customer', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     # class Meta:
#     #     managed = False
#     #     db_table = 'ProjectDetail'

# class Subdepartment_EstimatingDB(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
#     linenumber = models.IntegerField(db_column='LineNumber')  # Field name made lowercase.
#     description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

#     # class Meta:
#     #     managed = False
#     #     db_table = 'SubDepartment'

    
# class Departmentalforcatsedhour_EstimatingDB(models.Model):
#     # id = models.AutoField(db_column='ID')  # Field name made lowercase.
#     projectnumber = models.CharField(db_column='ProjectNumber', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     subdepartmentid = models.ForeignKey('Subdepartment', models.DO_NOTHING, db_column='SubDepartmentID')  # Field name made lowercase.
#     description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     quoteid = models.IntegerField(db_column='QuoteId')  # Field name made lowercase.
#     quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
#     unit = models.CharField(db_column='Unit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     unitcost = models.DecimalField(db_column='UnitCost', max_digits=15, decimal_places=2)  # Field name made lowercase.
#     costamount = models.DecimalField(db_column='CostAmount', max_digits=15, decimal_places=2)  # Field name made lowercase.
#     currency = models.CharField(db_column='Currency', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     priceunit = models.CharField(db_column='PriceUnit', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#     updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
#     revisionnumber = models.IntegerField(db_column='RevisionNumber', blank=True, null=True)  # Field name made lowercase.
#     projectversionid = models.IntegerField(db_column='ProjectVersionId', blank=True, null=True)  # Field name made lowercase.
#     projectdescription = models.TextField(db_column='ProjectDescription', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     projectdetailid = models.ForeignKey('Projectdetail', models.DO_NOTHING, db_column='ProjectDetailId', blank=True, null=True)  # Field name made lowercase.

#     # class Meta:
#     #     managed = False
#     #     db_table = 'DepartmentalForcatsedHour'

class Bookings(models.Model):
    hubplannerResourceId = models.CharField(max_length=255)
    hubplannerProjectId = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    totalHour = models.DecimalField(max_digits=15, decimal_places=2)
    stateValue = models.DecimalField(max_digits=15, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    bookingId = models.CharField(max_length=255, default='0000000000')
    projectId = models.IntegerField(blank=True, null=True)
    personId = models.IntegerField(blank=True, null=True)
    createdDate = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)


class Department(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    divisionid = models.ForeignKey('Division', models.DO_NOTHING, db_column='DivisionID')  # Field name made lowercase.
    hubplannerid = models.CharField(db_column='HubPlannerID', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.

class Person(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mhsemail = models.CharField(db_column='MHSEmail', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fortnaemail = models.CharField(db_column='FortnaEmail', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    departmentid = models.ForeignKey(Department, models.DO_NOTHING, db_column='DepartmentID')  # Field name made lowercase.
    personstatus = models.CharField(db_column='PersonStatus', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    hubplannerid = models.CharField(db_column='HubPlannerID', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.
    eeid = models.IntegerField(db_column='EEID', blank=True, null=True)  # Field name made lowercase.

class Customer(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.
    hubplannercustomerid = models.CharField(db_column='HubplannerCustomerID', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

class Division(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.

class Currencytype(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    symbol = models.CharField(db_column='Symbol', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    shortname = models.CharField(db_column='Shortname', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.

class Projecttype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.
    lastmodifiedby = models.CharField(db_column='LastModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

class Projectstage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.
    lastmodifiedby = models.CharField(db_column='LastModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

class Projectcategory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.
    lastmodifiedby = models.CharField(db_column='LastModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

class Site(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='Zipcode', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    custid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustID', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.


class Project(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    objective = models.TextField(db_column='Objective', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerID')  # Field name made lowercase.
    siteid = models.ForeignKey('Site', models.DO_NOTHING, db_column='SiteID')  # Field name made lowercase.
    divisionid = models.ForeignKey(Division, models.DO_NOTHING, db_column='DivisionID')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validfrom = models.DateTimeField(db_column='ValidFrom')  # Field name made lowercase.
    validto = models.DateTimeField(db_column='ValidTo')  # Field name made lowercase.
    hubplannerprojectid = models.CharField(db_column='HubplannerProjectID', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    projecttypeid = models.ForeignKey('Projecttype', models.DO_NOTHING, db_column='ProjectTypeID')  # Field name made lowercase.
    projectstageid = models.ForeignKey('Projectstage', models.DO_NOTHING, db_column='ProjectStageID')  # Field name made lowercase.
    projectcategoryid = models.ForeignKey('Projectcategory', models.DO_NOTHING, db_column='ProjectCategoryID')  # Field name made lowercase.
    currencytypeid = models.ForeignKey(Currencytype, models.DO_NOTHING, db_column='CurrencyTypeId', blank=True, null=True)  # Field name made lowercase.
    stage = models.CharField(db_column='Stage', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.


