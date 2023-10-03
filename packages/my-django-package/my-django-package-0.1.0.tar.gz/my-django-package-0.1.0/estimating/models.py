# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Departmentalforcatsedhour(models.Model):
    # id = models.AutoField(db_column='ID')  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    subdepartmentid = models.ForeignKey('Subdepartment', models.DO_NOTHING, db_column='SubDepartmentID')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    quoteid = models.IntegerField(db_column='QuoteId')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=15, decimal_places=2)  # Field name made lowercase.
    costamount = models.DecimalField(db_column='CostAmount', max_digits=15, decimal_places=2)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    priceunit = models.CharField(db_column='PriceUnit', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
    revisionnumber = models.IntegerField(db_column='RevisionNumber', blank=True, null=True)  # Field name made lowercase.
    # baseversion = models.IntegerField(db_column='BaseVersion', blank=True, null=True)  # Field name made lowercase.
    # optionversion = models.IntegerField(db_column='OptionVersion', blank=True, null=True)  # Field name made lowercase.
    projectversionid = models.IntegerField(db_column='ProjectVersionId', blank=True, null=True)  # Field name made lowercase.
    projectdescription = models.TextField(db_column='ProjectDescription', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    projectdetailid = models.ForeignKey('Projectdetail', models.DO_NOTHING, db_column='ProjectDetailId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DepartmentalForcatsedHour'


# class Notes(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     projectid = models.IntegerField(db_column='ProjectID', blank=True, null=True)  # Field name made lowercase.
#     createddate = models.DateField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#     createdby = models.CharField(db_column='CreatedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     note = models.TextField(db_column='Note', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     sharepointid = models.IntegerField(db_column='SharepointID', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'Notes'


class Projectdetail(models.Model):
    # id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    projectnumber = models.CharField(db_column='ProjectNumber', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    revisionnumber = models.IntegerField(db_column='RevisionNumber')  # Field name made lowercase.
    baseversion = models.CharField(db_column='BaseVersion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    totalcost = models.DecimalField(db_column='TotalCost', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalsell = models.DecimalField(db_column='TotalSell', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    blendedmargin = models.DecimalField(db_column='BlendedMargin', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True)  # Field name made lowercase.
    baseversiondescription = models.CharField(db_column='BaseVersionDescription', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    qouteid = models.IntegerField(db_column='QouteId')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    optionversion = models.CharField(db_column='OptionVersion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    optionversiondescription = models.CharField(db_column='OptionVersionDescription', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customer = models.CharField(db_column='Customer', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ProjectDetail'


# class Quoterequests(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     title = models.CharField(db_column='Title', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     createddate = models.DateField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#     createdby = models.CharField(db_column='CreatedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     createdbyemail = models.CharField(db_column='CreatedByEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     customerid = models.IntegerField(db_column='CustomerID', blank=True, null=True)  # Field name made lowercase.
#     customerlocations = models.CharField(db_column='CustomerLocations', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     quotetype = models.CharField(db_column='QuoteType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     duedate = models.DateField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
#     requeststate = models.CharField(db_column='RequestState', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     scopeofwork = models.TextField(db_column='ScopeOfWork', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     linktodocuments = models.TextField(db_column='LinkToDocuments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newcustomer = models.CharField(db_column='NewCustomer', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newsiteabbreviation = models.CharField(db_column='NewSiteAbbreviation', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newsiteaddress = models.CharField(db_column='NewSiteAddress', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newsitecity = models.CharField(db_column='NewSiteCity', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newsitecountry = models.CharField(db_column='NewSiteCountry', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newsitestate = models.CharField(db_column='NewSiteState', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     newsitezipcode = models.CharField(db_column='NewSiteZipCode', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'QuoteRequests'


class Subdepartment(models.Model):
    # id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    linenumber = models.IntegerField(db_column='LineNumber')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SubDepartment'


# class Sysdiagrams(models.Model):
#     name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     principal_id = models.IntegerField()
#     diagram_id = models.AutoField(primary_key=True)
#     version = models.IntegerField(blank=True, null=True)
#     definition = models.BinaryField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'sysdiagrams'
#         unique_together = (('principal_id', 'name'),)


# class Tbugtracking(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     screen = models.CharField(db_column='Screen', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     description = models.TextField(db_column='Description', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     notes = models.TextField(db_column='Notes', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     status = models.CharField(db_column='Status', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     priority = models.CharField(db_column='Priority', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     createdby = models.CharField(db_column='CreatedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     createddate = models.DateField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#     closeddate = models.DateField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tBugTracking'


# class Tcountries(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     country = models.CharField(db_column='Country', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tCountries'


# class Tcustomercontacts(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     customer = models.ForeignKey('Tcustomername', models.DO_NOTHING, db_column='customer_ID', blank=True, null=True)  # Field name made lowercase.
#     location = models.ForeignKey('Tcustomerlocation', models.DO_NOTHING, db_column='location_ID', blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     phone_number = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     job_title = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tCustomerContacts'


# class Tcustomerlegacytype(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tCustomerLegacyType'


# class Tcustomerlocation(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     site_abbreviation = models.CharField(db_column='Site_Abbreviation', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     address_line_1 = models.CharField(db_column='Address_Line_1', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     address_line_2 = models.CharField(db_column='Address_Line_2', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     city = models.CharField(db_column='City', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     zip_code = models.CharField(db_column='Zip_Code', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     country = models.CharField(db_column='Country', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     customerid = models.ForeignKey('Tcustomername', models.DO_NOTHING, db_column='CustomerID', blank=True, null=True)  # Field name made lowercase.
#     customer = models.CharField(db_column='Customer', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     stateid = models.ForeignKey('Tstatesandcountries', models.DO_NOTHING, db_column='StateID', blank=True, null=True)  # Field name made lowercase.
#     state = models.CharField(db_column='State', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     notes = models.TextField(db_column='Notes', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tCustomerLocation'


# class Tcustomerlocationreference(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     locationid = models.ForeignKey(Tcustomerlocation, models.DO_NOTHING, db_column='LocationID', blank=True, null=True)  # Field name made lowercase.
#     former_project_group = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     contact_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     contact_email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tCustomerLocationReference'


# class Tcustomername(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     customername = models.CharField(db_column='CustomerName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     legalname = models.CharField(db_column='LegalName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     logo = models.BinaryField(db_column='Logo', blank=True, null=True)  # Field name made lowercase.
#     legacytype = models.ForeignKey(Tcustomerlegacytype, models.DO_NOTHING, db_column='LegacyType', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tCustomerName'


# class Tdepartment(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     department = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tDepartment'


# class Testimatorstatus(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     status = models.CharField(db_column='Status', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tEstimatorStatus'


# class Testimatortype(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     labortype = models.CharField(db_column='LaborType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tEstimatorType'


# class Tmachinetype(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     machine_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tMachineType'


# class Tnotedeletebyuser(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     username = models.TextField(db_column='Username', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     userid = models.TextField(db_column='UserID', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     projectid = models.ForeignKey('Tquotelog', models.DO_NOTHING, db_column='ProjectID', blank=True, null=True)  # Field name made lowercase.
#     noteid = models.IntegerField(db_column='NoteID', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tNoteDeleteByUser'


# class Torderentrystatus(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     order_entry_status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tOrderEntryStatus'


# class Tpeople(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     fullname = models.CharField(db_column='FullName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     email = models.CharField(db_column='Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tPeople'


# class Tprojecttype(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     project_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tProjectType'


# class Tquoteapprovals(models.Model):
#     id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
#     quoteid = models.ForeignKey('Tquotelog', models.DO_NOTHING, db_column='QuoteID', blank=True, null=True)  # Field name made lowercase.
#     cost = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     sell = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     approver_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     approver_email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tQuoteApprovals'


# class Tquotecosts(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     quoteid = models.ForeignKey('Tquotelog', models.DO_NOTHING, db_column='quoteID', blank=True, null=True)  # Field name made lowercase.
#     jobnumber = models.CharField(db_column='JobNumber', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     line = models.IntegerField(blank=True, null=True)
#     wbscostcode = models.CharField(db_column='wbsCostCode', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     costobject = models.CharField(db_column='costObject', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     description = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     quantity = models.FloatField(blank=True, null=True)
#     unit = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     unitcost = models.DecimalField(db_column='unitCost', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     costamount = models.DecimalField(db_column='costAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     currency = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     priceunit = models.CharField(db_column='priceUnit', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tQuoteCosts'


# class Tquotecurrentstate(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     current_state = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tQuoteCurrentState'


# class Tquoteequipmentdetails(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     option = models.ForeignKey('Tquoteoptioncosts', models.DO_NOTHING, db_column='option_ID', blank=True, null=True)  # Field name made lowercase.
#     machine_type = models.ForeignKey(Tmachinetype, models.DO_NOTHING, db_column='machine_type', blank=True, null=True)
#     machine_qty = models.IntegerField(blank=True, null=True)
#     machine_detail = models.IntegerField(blank=True, null=True)
#     detail_uom_id = models.IntegerField(db_column='detail_UOM_ID', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tQuoteEquipmentDetails'


# class Tquoteestimators(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     quoteid = models.ForeignKey('Tquotelog', models.DO_NOTHING, db_column='QuoteID', blank=True, null=True)  # Field name made lowercase.
#     estimatortype = models.ForeignKey(Testimatortype, models.DO_NOTHING, db_column='EstimatorType', blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField(db_column='Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     email = models.CharField(db_column='Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
#     duedate = models.DateField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
#     status = models.ForeignKey(Testimatorstatus, models.DO_NOTHING, db_column='Status', blank=True, null=True)  # Field name made lowercase.
#     completeddate = models.DateField(db_column='CompletedDate', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tQuoteEstimators'


# class Tquotegroups(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     group_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tQuoteGroups'


# class Tquotelog(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     rev = models.IntegerField(db_column='Rev', blank=True, null=True)  # Field name made lowercase.
#     recieveddate = models.DateField(db_column='RecievedDate', blank=True, null=True)  # Field name made lowercase.
#     duedate = models.DateField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
#     completeddate = models.DateField(db_column='CompletedDate', blank=True, null=True)  # Field name made lowercase.
#     modifieddate = models.DateField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
#     scopeofwork = models.TextField(db_column='ScopeOfWork', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     estimatedprice = models.DecimalField(db_column='EstimatedPrice', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     purchasedprice = models.DecimalField(db_column='PurchasedPrice', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     customer = models.ForeignKey(Tcustomername, models.DO_NOTHING, db_column='Customer', blank=True, null=True)  # Field name made lowercase.
#     locations = models.TextField(db_column='Locations', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     quotestatus = models.ForeignKey('Tquotestatus', models.DO_NOTHING, db_column='QuoteStatus', blank=True, null=True)  # Field name made lowercase.
#     salestatus = models.ForeignKey('Tsalestatus', models.DO_NOTHING, db_column='SaleStatus', blank=True, null=True)  # Field name made lowercase.
#     turnoverstatus = models.ForeignKey('Tturnoverstatus', models.DO_NOTHING, db_column='TurnoverStatus', blank=True, null=True)  # Field name made lowercase.
#     orderentrystatus = models.ForeignKey(Torderentrystatus, models.DO_NOTHING, db_column='OrderEntryStatus', blank=True, null=True)  # Field name made lowercase.
#     department = models.ForeignKey(Tdepartment, models.DO_NOTHING, db_column='Department', blank=True, null=True)  # Field name made lowercase.
#     type = models.ForeignKey('Ttype', models.DO_NOTHING, db_column='Type', blank=True, null=True)  # Field name made lowercase.
#     quotetype = models.ForeignKey('Tquotetype', models.DO_NOTHING, db_column='QuoteType', blank=True, null=True)  # Field name made lowercase.
#     projecttype = models.ForeignKey(Tprojecttype, models.DO_NOTHING, db_column='ProjectType', blank=True, null=True)  # Field name made lowercase.
#     currentstate = models.ForeignKey(Tquotecurrentstate, models.DO_NOTHING, db_column='CurrentState', blank=True, null=True)  # Field name made lowercase.
#     jobnumber = models.CharField(db_column='JobNumber', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     sharepointid = models.IntegerField(db_column='SharepointID', blank=True, null=True)  # Field name made lowercase.
#     accepteddate = models.DateField(db_column='AcceptedDate', blank=True, null=True)  # Field name made lowercase.
#     emailleadtoturnover = models.BooleanField(db_column='EmailLeadtoTurnover', blank=True, null=True)  # Field name made lowercase.
#     leadestimator = models.CharField(db_column='LeadEstimator', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     mechanicalestimator = models.CharField(db_column='MechanicalEstimator', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     electricalestimator = models.CharField(db_column='ElectricalEstimator', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     salesrep = models.CharField(db_column='SalesRep', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     systemengineer = models.CharField(db_column='SystemEngineer', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     proposalmanager = models.CharField(db_column='ProposalManager', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     leadestimatoremail = models.CharField(db_column='LeadEstimatorEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     mechestimatoremail = models.CharField(db_column='MechEstimatorEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     elecestimatoremail = models.CharField(db_column='ElecEstimatorEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     salesrepemail = models.CharField(db_column='SalesRepEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     systemengineeremail = models.CharField(db_column='SystemEngineerEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     proposalmanageremail = models.CharField(db_column='ProposalManagerEmail', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     purchaseorderdate = models.DateField(db_column='PurchaseOrderDate', blank=True, null=True)  # Field name made lowercase.
#     revisionreasonid = models.ForeignKey('Tquoterevisionreasons', models.DO_NOTHING, db_column='RevisionReasonID', blank=True, null=True)  # Field name made lowercase.
#     holdreviewdate = models.DateField(db_column='HoldReviewDate', blank=True, null=True)  # Field name made lowercase.
#     groupid = models.ForeignKey(Tquotegroups, models.DO_NOTHING, db_column='GroupID', blank=True, null=True)  # Field name made lowercase.
#     projectid = models.IntegerField(db_column='ProjectID', blank=True, null=True)  # Field name made lowercase.
#     approveddate = models.DateField(db_column='ApprovedDate', blank=True, null=True)  # Field name made lowercase.
#     priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
#     costingdata = models.TextField(db_column='CostingData', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     harddeadline = models.BooleanField(db_column='HardDeadline', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tQuoteLog'


# class Tquoteloglocations(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     projectid = models.IntegerField(db_column='ProjectID', blank=True, null=True)  # Field name made lowercase.
#     locationid = models.ForeignKey(Tcustomerlocation, models.DO_NOTHING, db_column='LocationID', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tQuoteLogLocations'


# class Tquoteoptioncosts(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     projectid = models.ForeignKey(Tquotelog, models.DO_NOTHING, db_column='ProjectID', blank=True, null=True)  # Field name made lowercase.
#     versionbasenumber = models.IntegerField(db_column='VersionBaseNumber', blank=True, null=True)  # Field name made lowercase.
#     versionoptionnumber = models.IntegerField(db_column='VersionOptionNumber', blank=True, null=True)  # Field name made lowercase.
#     versionprice = models.DecimalField(db_column='VersionPrice', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     versiondescription = models.TextField(db_column='VersionDescription', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     cost = models.DecimalField(db_column='Cost', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tQuoteOptionCosts'


# class Tquoterevisionreasons(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     revision_reason = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tQuoteRevisionReasons'


# class Tquotestatus(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     quote_status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tQuoteStatus'


# class Tquotetype(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     quote_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tQuoteType'


# class Tsalestatus(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     sale_status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSaleStatus'


# class Tstatesandcountries(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     title = models.CharField(db_column='Title', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
#     abbreviation = models.CharField(db_column='Abbreviation', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     country = models.CharField(db_column='Country', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tStatesAndCountries'


# class TstatsDailycount(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     date = models.DateField(db_column='Date')  # Field name made lowercase.
#     napactive = models.IntegerField(db_column='NAPActive')  # Field name made lowercase.
#     napcompleted = models.IntegerField(db_column='NAPCompleted')  # Field name made lowercase.
#     napcancelled = models.IntegerField(db_column='NAPCancelled')  # Field name made lowercase.
#     naponhold = models.IntegerField(db_column='NAPOnHold')  # Field name made lowercase.
#     lpsactive = models.IntegerField(db_column='LPSActive')  # Field name made lowercase.
#     lpscompleted = models.IntegerField(db_column='LPSCompleted')  # Field name made lowercase.
#     lpscancelled = models.IntegerField(db_column='LPSCancelled')  # Field name made lowercase.
#     lpsonhold = models.IntegerField(db_column='LPSOnHold')  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tStats_DailyCount'


# class Tsubcontractquotes(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     quote = models.ForeignKey(Tquotelog, models.DO_NOTHING, db_column='quote_ID', blank=True, null=True)  # Field name made lowercase.
#     subcontactor = models.ForeignKey('Tsubcontractors', models.DO_NOTHING, db_column='subcontactor_ID', blank=True, null=True)  # Field name made lowercase.
#     service_type = models.IntegerField(blank=True, null=True)
#     accepted = models.BooleanField(blank=True, null=True)
#     awarded = models.BooleanField(blank=True, null=True)
#     winner = models.BooleanField(blank=True, null=True)
#     requested_date = models.DateField(blank=True, null=True)
#     received_date = models.DateField(blank=True, null=True)
#     expiration_date = models.DateField(blank=True, null=True)
#     updated_bid_date = models.DateField(blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     total_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSubcontractQuotes'


# class Tsubcontractorcontacts(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     subcontractor = models.ForeignKey('Tsubcontractors', models.DO_NOTHING, db_column='subcontractor_ID', blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     phone_number = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     job_title = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSubcontractorContacts'


# class Tsubcontractordiscipline(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     discipline = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSubcontractorDiscipline'


# class Tsubcontractorrating(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     sub = models.ForeignKey('Tsubcontractors', models.DO_NOTHING, db_column='sub_ID', blank=True, null=True)  # Field name made lowercase.
#     rating = models.FloatField(blank=True, null=True)
#     rated_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     rated_by_email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     comment = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSubcontractorRating'


# class Tsubcontractors(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     company_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     discipline = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     city = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     phone_number = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     website = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     created_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     state_id = models.IntegerField(db_column='state_ID', blank=True, null=True)  # Field name made lowercase.
#     price_rating = models.IntegerField(blank=True, null=True)
#     quality_rating = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSubcontractors'


# class Tsuppliercontacts(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     supplier = models.ForeignKey('Tsuppliers', models.DO_NOTHING, db_column='supplier_ID', blank=True, null=True)  # Field name made lowercase.
#     name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     phone_number = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     job_title = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSupplierContacts'


# class Tsupplierquotes(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     quote = models.ForeignKey(Tquotelog, models.DO_NOTHING, db_column='quote_ID', blank=True, null=True)  # Field name made lowercase.
#     supplier = models.ForeignKey('Tsuppliers', models.DO_NOTHING, db_column='supplier_ID', blank=True, null=True)  # Field name made lowercase.
#     service_type = models.IntegerField(blank=True, null=True)
#     accepted = models.BooleanField(blank=True, null=True)
#     awarded = models.BooleanField(blank=True, null=True)
#     winner = models.BooleanField(blank=True, null=True)
#     requested_date = models.DateField(blank=True, null=True)
#     received_date = models.DateField(blank=True, null=True)
#     expiration_date = models.DateField(blank=True, null=True)
#     updated_bid_date = models.DateField(blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     total_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSupplierQuotes'


# class Tsupplierrating(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     supplier = models.ForeignKey('Tsuppliers', models.DO_NOTHING, db_column='supplier_ID', blank=True, null=True)  # Field name made lowercase.
#     rating = models.FloatField(blank=True, null=True)
#     rated_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     rated_by_email = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     comment = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSupplierRating'


# class Tsuppliers(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     company_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     discipline = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     city = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     phone_number = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     website = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     created_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     notes = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     state_id = models.IntegerField(db_column='state_ID', blank=True, null=True)  # Field name made lowercase.
#     price_rating = models.IntegerField(blank=True, null=True)
#     quality_rating = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tSuppliers'


# class Tturnoverstatus(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     turnover_status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tTurnoverStatus'


# class Ttype(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'tType'


# class Tusers(models.Model):
#     id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     o365id = models.CharField(db_column='O365ID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     displayname = models.CharField(db_column='DisplayName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     email = models.CharField(db_column='Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     department = models.CharField(db_column='Department', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     jobtitle = models.CharField(db_column='JobTitle', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     officelocation = models.CharField(db_column='OfficeLocation', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
#     accesslevel = models.IntegerField(db_column='AccessLevel', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'tUsers'
