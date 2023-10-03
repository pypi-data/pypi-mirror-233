from datetime import datetime
import decimal
import json
import math
from django.shortcuts import render
from . import salesforce
from logger.logger import LoggerView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from salesforce.models import SalesforceOppportunity
from rest_framework import request
from salesforce.api.paginations import CustomPagination
from rest_framework.generics import ListAPIView
from salesforce.api.serializers import SalesforceOppportunityOGSerializer
from django.db.models import QuerySet

# Create your views here.

@api_view()
def getAccounts(request):
    log = LoggerView(log_file='log.log')
    results = salesforce.sf.query("SELECT Id, Name,Type, BillingAddress, CurrencyIsoCode, OwnerId FROM Account")
    accounts = results['records']
    log.logger.info(accounts)
    print(accounts)
    return  Response(accounts)

@api_view()
def getSobjects(request):
    # log = LoggerView(log_file='log.log')
    results = salesforce.sf.query("SELECT  QualifiedApiName FROM EntityDefinition order by QualifiedApiName")
    objectList = results['records']
    # log.logger.info(accounts)
    # print(accounts)
    return Response(objectList)

@api_view()
def getFieldName(request,sobject):
    # log = LoggerView(log_file='log.log')
    results = salesforce.sf.query("SELECT  QualifiedApiName FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName = '"+sobject+"'")
    accounts = results['records']
    # log.logger.info(accounts)
    # print(accounts)
    return Response(accounts)


class OpportunityListView(ListAPIView):
    results = salesforce.sf.query("SELECT \
    Id, Name, Description, AccountId, Account_Owner__c, OwnerId, Owner.Name, RecordTypeId, RecordType.Name, StageName, Amount, Probability, \
    ExpectedRevenue, CloseDate, Type, IsWon, CurrencyIsoCode, ProjectID__c, \
    ForecastCategoryName, EstimatedWeeks__c, Sales_Team__c, Service_Area_Lvl_1__c, Service_Level_1__c,\
    Service_Type__c, Project_Type__c, Project_Start_Date__c, Go_Live_Date__c, \
    Occur_Probability__c, Win_Probability__c, Estimate_Completion_Date__c, \
    Currency__c, Probable_Gross_Profit__c, LPS_Sale_Number__c,\
    Account.Id, Account.Name, Account.BillingAddress\
    FROM Opportunity where Service_Level_1__c in ('LPS Services' , 'LPS Projects' , 'LPS Parts' , 'LPS Tech Support' , 'LPS Lifecycle Contracts') ")
    # salesforce.sf.query("SELECT Id, Name, AccountId,OwnerId, RecordTypeId, StageName, Amount, Probability, ExpectedRevenue, CloseDate, Type, IsWon, CurrencyIsoCode, ProjectID__c,ForecastCategoryName,EstimatedWeeks__c, Sales_Team__c,Service_Area_Lvl_1__c,Service_Type__c,Project_Type__c,Project_Start_Date__c,Go_Live_Date__c,\
    #                               Occur_Probability__c,Win_Probability__c,Estimate_Completion_Date__c,Currency__c,Probable_Gross_Profit__c,LPS_Sale_Number__c, \
    #                               (Select name, BillingAddress from Account) FROM Opportunity")
    print(len( results['records']))

    queryset =  list(results['records'])
    # print(queryset)
    serializer_class = SalesforceOppportunityOGSerializer
    pagination_class = CustomPagination
    # opportunities = paginator.get_paginated_response(results['records'])
    # return Response(opportunities)
@api_view()
def getOpportunity(request):
    page = int(request.GET.get('page',1))
    per_page = 100

    opportunities = getAllOPportunity()
    total = len(opportunities)
    start = (page-1) * per_page
    end = page * per_page

    opportunityList = opportunities[start:end]
    
    return Response({
        'data': opportunityList,
        'total': total,
        'page': page,
        'last_page' : math.ceil(total / per_page)
    })

def getAllOPportunity():
    results = salesforce.sf.query_all("SELECT \
    Id, Name, Description, AccountId, Account_Owner__c, OwnerId, Owner.Name, RecordTypeId, RecordType.Name, StageName, Amount, Probability, \
    ExpectedRevenue, CloseDate, Type, IsWon, CurrencyIsoCode, ProjectID__c, \
    ForecastCategoryName, EstimatedWeeks__c, Sales_Team__c, Service_Area_Lvl_1__c, Service_Level_1__c,\
    Service_Type__c, Project_Type__c, Project_Start_Date__c, Go_Live_Date__c, \
    Occur_Probability__c, Win_Probability__c, Estimate_Completion_Date__c, \
    Currency__c, Probable_Gross_Profit__c, LPS_Sale_Number__c,\
    Account.Id, Account.Name, Account.BillingAddress,CreatedDate,LastModifiedDate\
    FROM Opportunity where Service_Level_1__c in ('LPS Services' , 'LPS Projects', 'LPS Parts' , 'LPS Tech Support' , 'LPS Lifecycle Contracts') ")
    
    # salesforce.sf.query("SELECT Id, Name, AccountId,OwnerId, RecordTypeId, StageName, Amount, Probability, ExpectedRevenue, CloseDate, Type, IsWon, CurrencyIsoCode, ProjectID__c,ForecastCategoryName,EstimatedWeeks__c, Sales_Team__c,Service_Area_Lvl_1__c,Service_Type__c,Project_Type__c,Project_Start_Date__c,Go_Live_Date__c,\
    #                               Occur_Probability__c,Win_Probability__c,Estimate_Completion_Date__c,Currency__c,Probable_Gross_Profit__c,LPS_Sale_Number__c, \
    #                               (Select name, BillingAddress from Account) FROM Opportunity")
    opportunities = results['records']
    print(len(opportunities))
    # print(opportunities)
    return opportunities

def generateAddress(address):
    if(address is not None and address['street'] is not None and address['city'] is not None and address['stateCode'] is not None and address['countryCode'] is not None and address['postalCode'] is not None):
        return address['street']+" "+address['city']+" "+address['stateCode']+" "+address['countryCode']+" "+address['postalCode']
    elif(address is not None and address['city'] is not None and address['stateCode'] is not None and address['countryCode'] and address['postalCode'] is not None):
        return address['city']+" "+address['stateCode']+" "+address['countryCode']+" "+address['postalCode']
    elif(address is not None and address['stateCode'] is not None and address['countryCode'] and address['postalCode'] is not None):
        return address['stateCode']+" "+address['countryCode']+" "+address['postalCode']
    elif(address is not None and address['stateCode'] is not None and address['countryCode']):
        return address['stateCode']+" "+address['countryCode']
    else :
        return ""
@api_view()
def AddOrUpdateOpportunity(request):
    opportunities = getAllOPportunity()
    createOpportunityList = []
    updateOpportunityList = []
    for opportunity in opportunities:
     
        opp = SalesforceOppportunity(
            SalesforceId = opportunity.get('Id'),
            Name = opportunity.get('Name'),
            Description = opportunity.get('Description'),
            CustomerName = opportunity['Account']['Name'],
            CustomerAddress = generateAddress(opportunity['Account']['BillingAddress']),
            OwnerName = opportunity['Owner']['Name'],
            StageName = opportunity.get('StageName'),
            Amount = decimal.Decimal(opportunity.get('Amount')),
            ServiceLevel1 = opportunity.get('Service_Level_1__c'),
            ExpectedRevenue = decimal.Decimal(opportunity.get('ExpectedRevenue')),
            CloseDate = opportunity.get('CloseDate'),
            IsWon = opportunity.get('IsWon'),
            CurrencyIsoCode = opportunity.get('CurrencyIsoCode'),
            StartDate = opportunity.get('Project_Start_Date__c'),
            GoLiveDate = opportunity.get('Go_Live_Date__c'),
            OccurProbability = decimal.Decimal(opportunity.get('Occur_Probability__c').split("%")[0]),
            WinProbability = decimal.Decimal(opportunity.get('Win_Probability__c').split("%")[0]),
            GrossProfit = decimal.Decimal(opportunity.get('Probable_Gross_Profit__c')),
            SalesforceCreatedDate = opportunity.get('CreatedDate'),
            SalesforceUpdatedDate = opportunity.get('LastModifiedDate')
        )
        # print(opp.CustomerAddress)
        if SalesforceOppportunity.objects.filter(SalesforceId = opportunity.get('Id')).count() > 0:
            opp.UpdatedDate = datetime.now()
            updateOpportunityList.append(opp)
        else:
            opp.CreatedDate = datetime.now()
            createOpportunityList.append(opp)
        
    print(len(createOpportunityList))
    print(len(updateOpportunityList))
    # Insert salesforce data into DB
    if(len(createOpportunityList) > 0):
     SalesforceOppportunity.objects.bulk_create(createOpportunityList)
    if(len(updateOpportunityList) > 0):
        updateOpportunity(updateOpportunityList)
    result = "created Opportunities " + str(len(createOpportunityList)) + " updated opportunities " + str(len(updateOpportunityList))
    return Response(result)

def updateOpportunity(updateOpportunityList):
    for opportunity in updateOpportunityList:
        opp = SalesforceOppportunity.objects.get(SalesforceId = opportunity.SalesforceId)
        # opp = opportunity
        if(opp.SalesforceUpdatedDate != opportunity.SalesforceUpdatedDate):
            opp.Name = opportunity.Name
            opp.Description = opportunity.Description
            opp.CustomerName = opportunity.CustomerName
            opp.CustomerAddress = opportunity.CustomerAddress
            opp.OwnerName = opportunity.OwnerName
            opp.StageName = opportunity.StageName
            opp.Amount = opportunity.Amount
            opp.ServiceLevel1 = opportunity.ServiceLevel1
            opp.ExpectedRevenue = opportunity.ExpectedRevenue
            opp.CloseDate = opportunity.CloseDate
            opp.IsWon = opportunity.IsWon
            opp.CurrencyIsoCode = opportunity.CurrencyIsoCode
            opp.StartDate = opportunity.StartDate
            opp.GoLiveDate = opportunity.GoLiveDate
            opp.OccurProbability = opportunity.OccurProbability
            opp.WinProbability = opportunity.WinProbability
            opp.GrossProfit = opportunity.GrossProfit
            opp.SalesforceCreatedDate = opportunity.SalesforceCreatedDate
            opp.SalesforceUpdatedDate = opportunity.SalesforceUpdatedDate
            opp.UpdatedDate = datetime.now()
            opp.save()
        

@api_view(['POST','PATCH'])
def getNewOpportunity(request):
    # data = json.loads(request.body)
    print("data",request.data)
    return Response(request.data)
    
def trigger_function(message, session_id):
    # Process the trigger event
    print('Trigger received:', message)
    print('Session ID:', session_id)