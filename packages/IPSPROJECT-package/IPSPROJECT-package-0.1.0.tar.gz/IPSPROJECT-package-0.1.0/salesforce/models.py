from django.db import models

# Create your models here.
class SalesforceOppportunity(models.Model):
    SalesforceId = models.CharField(max_length =20)
    ProjectNumber = models.CharField(max_length = 255,null=True)
    Name = models.CharField(max_length = 255)
    Description = models.TextField(null=True)
    CustomerName = models.CharField(max_length = 255)
    CustomerAddress = models.CharField(max_length = 255,null=True)
    OwnerName = models.CharField(max_length = 255)
    StageName = models.CharField(max_length = 100)
    Amount = models.DecimalField(max_digits = 15,decimal_places = 2)
    ServiceLevel1 =  models.CharField(max_length = 255,null=True)
    Probability = models.DecimalField(max_digits = 5,decimal_places = 2,null=True)
    ExpectedRevenue = models.DecimalField(max_digits = 15,decimal_places = 2)
    CloseDate = models.DateField(null=True)
    IsWon = models.BooleanField()
    CurrencyIsoCode = models.CharField(max_length=5)
    StartDate = models.DateField(null=True)
    GoLiveDate = models.DateField(null=True)
    OccurProbability = models.DecimalField(max_digits = 5,decimal_places = 2)
    WinProbability = models.DecimalField(max_digits = 5,decimal_places = 2)
    GrossProfit = models.DecimalField(max_digits = 15,decimal_places = 2)
    SalesforceCreatedDate = models.DateTimeField(null=True)
    SalesforceUpdatedDate = models.DateTimeField(null=True)
    CreatedDate = models.DateTimeField(null=True)
    UpdatedDate = models.DateTimeField(null=True)

class Attributes(models.Model):
      type = models.CharField(max_length = 255),
      url = models.CharField(max_length = 255)

class RecordType(models.Model):
    attributes = Attributes,
    Name = models.CharField(max_length = 255)

class BillingAddress (models.Model):
    city = models.CharField(max_length = 255),
    country = models.CharField(max_length = 255),
    countryCode = models.CharField(max_length = 255),
    geocodeAccuracy = models.CharField(max_length = 255),
    latitude = models.CharField(max_length = 255),
    longitude = models.CharField(max_length = 255),
    postalCode = models.CharField(max_length = 255),
    state = models.CharField(max_length = 255),
    stateCode = models.CharField(max_length = 255),
    street = models.CharField(max_length = 255)

class Account(models.Model):
    attributes = Attributes,
    Id = models.CharField(max_length = 255),
    Name = models.CharField(max_length = 255),
    BillingAddress = BillingAddress

class SalesforceOpportunityOG(models.Model):
 
        attributes = Attributes,
        Id =  models.CharField(max_length = 255),
        Name =  models.CharField(max_length = 255),
        Description = models.CharField(max_length = 255),
        AccountId = models.CharField(max_length = 255),
        Account_Owner__c = models.CharField(max_length = 255),
        OwnerId = models.CharField(max_length = 255),
        Owner = RecordType,
        RecordTypeId = models.CharField(max_length = 255),
        RecordType = RecordType,
        StageName = models.CharField(max_length = 255),
        Amount =  models.DecimalField(max_digits = 15,decimal_places = 2),
        Probability =  models.DecimalField(max_digits = 5,decimal_places = 2),
        ExpectedRevenue =  models.DecimalField(max_digits = 15,decimal_places = 2),
        CloseDate = models.DateTimeField(null=True),
        Type = models.CharField(max_length = 255),
        IsWon =  models.BooleanField(),
        CurrencyIsoCode = models.CharField(max_length = 255),
        ProjectID__c = models.CharField(max_length = 255),
        ForecastCategoryName = models.CharField(max_length = 255),
        EstimatedWeeks__c = models.CharField(max_length = 255),
        Sales_Team__c = models.CharField(max_length = 255),
        Service_Area_Lvl_1__c = models.CharField(max_length = 255),
        Service_Level_1__c =  models.CharField(max_length = 255),
        Service_Type__c = models.CharField(max_length = 255),
        Project_Type__c = models.CharField(max_length = 255),
        Project_Start_Date__c =  models.DateTimeField(null=True),
        Go_Live_Date__c =  models.DateTimeField(null=True),
        Occur_Probability__c = models.DecimalField(max_digits = 5,decimal_places = 2),
        Win_Probability__c = models.DecimalField(max_digits = 5,decimal_places = 2),
        Estimate_Completion_Date__c =  models.DateTimeField(null=True),
        Currency__c = models.CharField(max_length = 255),
        Probable_Gross_Profit__c = models.DecimalField(max_digits = 5,decimal_places = 2),
        LPS_Sale_Number__c = models.IntegerField(),
        Account = Account,
        CreatedDate = models.DateTimeField(null=True),
        LastModifiedDate = models.DateTimeField(null=True)
        


