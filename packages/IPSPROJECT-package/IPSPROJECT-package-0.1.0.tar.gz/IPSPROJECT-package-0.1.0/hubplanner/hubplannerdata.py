# HubPlanner API universal settings
import requests
import json
from logger.logger import LoggerView
from datetime import date, datetime, timedelta
from stopwatch import Stopwatch

HUBPLANNER_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6IlNDT1BFX1JFQURfV1JJVEUiLCJpc3MiOi"\
    "I1ZWY0ZmQ0MzkzMmRmNjAxMzNiMjZkNDQiLCJyZXNvdXJjZSI6IjVlYjFkMDU4ZTJhODhmMGI5ZDNjYTY5MiIsIml"\
    "hdCI6MTYxOTE4NDU5NX0.ps0eRDZHYeDSlAjnddZZMZbMDwVqEEwNlbbPhx04Ka8"
HUBPLANNER_ROOT_URL = "https://api.hubplanner.com/v1/"
HUBPLANNER_HEADERS = {'Authorization': HUBPLANNER_API_KEY,
        'Content-Type': 'application/json',
            'Accept': 'application/json'}

log = LoggerView(log_file='log.log') #logging.getLogger('hubplanner_forecasting')

# create and start stopwatches
# t = incremental stopwatch
# tt = full script stopwatch
t = Stopwatch()
tt = Stopwatch()

def getActiveResources():
    dictResources = {}
    rspGetResources = requests.get(f"{HUBPLANNER_ROOT_URL}resource", headers=HUBPLANNER_HEADERS)
    jsonGetResources = json.loads(rspGetResources.text)
    for resource in jsonGetResources:
        if resource['status'] == 'STATUS_ACTIVE':
            if (resource['useCustomAvailability'] == False):
                resource['customAvailabilities'] = {
                        'weekDays': {
                                        "monday": {
                                            "workDay": True,
                                            "minutes": 480
                                        },
                                        "tuesday": {
                                            "workDay": True,
                                            "minutes": 480
                                        },
                                        "wednesday": {
                                            "workDay": True,
                                            "minutes": 480
                                        },
                                        "thursday": {
                                            "workDay": True,
                                            "minutes": 480
                                        },
                                        "friday": {
                                            "workDay": True,
                                            "minutes": 480
                                        },
                                        "saturday": {
                                            "workDay": False,
                                            "minutes": 0
                                        },
                                        "sunday": {
                                            "workDay": False,
                                            "minutes": 0
                                        }
                                    },
                                '_id' : 'default'
                                }
            totalHoursCapacity = 0
            for weekDay in resource['customAvailabilities'].get('weekDays').values():
                if weekDay['minutes'] is None :
                    weekDay['minutes'] = 0
                totalHoursCapacity = float(totalHoursCapacity + (weekDay['minutes'] / 60))
            resource['totalHoursCapacity'] = totalHoursCapacity
            resource['fullName'] = (resource['firstName'] + ' ' + resource['lastName']).strip()
            dictResources[resource['_id']] = resource
    return dictResources
def getResourceGroups(resourceGroupParams):
    dictResourceGroups = {}
    for groupParams in resourceGroupParams:
        for groupID in groupParams['_ids']:
            rspGetResourceGroup = requests.get(
                f"{HUBPLANNER_ROOT_URL}resourcegroup/{groupID}", headers=HUBPLANNER_HEADERS)
            jsonGetResourceGroup = json.loads(rspGetResourceGroup.text)

            if groupParams['deptName'] not in dictResourceGroups.keys():
                dictResourceGroups[groupParams['deptName']] = jsonGetResourceGroup
            else:
                for resource in jsonGetResourceGroup['resources']:
                    tempGroup = dictResourceGroups[groupParams['deptName']]
                    if resource not in tempGroup['resources']:
                        tempGroup['resources'].append(resource)
    return dictResourceGroups
def getBookings(filterData = {}):
    dictBookings = {}
    PAGE_NUMBER = 0
    while True:
        rspGetBookings = requests.post(f"{HUBPLANNER_ROOT_URL}booking/search", headers=HUBPLANNER_HEADERS,
                                    params={'page': PAGE_NUMBER,
                                            'limit': '1000'},
                                    data=json.dumps(filterData)
                                    )
        jsonGetBookings = json.loads(rspGetBookings.text)
        for booking in jsonGetBookings:
            if booking['_id'] not in dictBookings.keys() and \
                    (booking['type'] == 'SCHEDULED' or booking['type'] == 'APPROVED'):
                booking['start'] = datetime.strptime(booking['start'], '%Y-%m-%dT%H:%M')
                booking['end'] = datetime.strptime(booking['end'], '%Y-%m-%dT%H:%M')
                dictBookings[booking['_id']] = booking
        if len(jsonGetBookings) < 1000:
            break
        PAGE_NUMBER = PAGE_NUMBER + 1
    return dictBookings
def getProjects():
    dictProjects = {}
    rspGetProjects = requests.get(f"{HUBPLANNER_ROOT_URL}project", headers=HUBPLANNER_HEADERS)
    jsonGetProjects = json.loads(rspGetProjects.text)
    for project in jsonGetProjects:
        dictProjects[project['_id']] = project
    return dictProjects
def getClients():
    dictClients = {}
    rspGetClients = requests.get(f"{HUBPLANNER_ROOT_URL}client", headers=HUBPLANNER_HEADERS)
    jsonGetClients = json.loads(rspGetClients.text)
    for client in jsonGetClients:
        dictClients[client['_id']] = client
    return dictClients
def getHolidays():
    dictHolidays = {}
    rspGetHolidays = requests.get(f"{HUBPLANNER_ROOT_URL}holiday", headers=HUBPLANNER_HEADERS)
    jsonGetHolidays = json.loads(rspGetHolidays.text)
    for holiday in jsonGetHolidays:
        #if datetime.strptime(holiday['date'], '%Y-%m-%d').year == date.today().year:
            dictHolidays[holiday['_id']] = holiday
    return getHolidays
def getEvents():
    dictEvents = {}
    rspGetEvents = requests.get(f"{HUBPLANNER_ROOT_URL}event", headers=HUBPLANNER_HEADERS)
    jsonGetEvents = json.loads(rspGetEvents.text)
    for event in jsonGetEvents:
        dictEvents[event['_id']] = event
    return dictEvents
def getVacations():
    dictVacations = {}
    rspGetVacations = requests.get(f"{HUBPLANNER_ROOT_URL}vacation", headers=HUBPLANNER_HEADERS)
    jsonGetVacations = json.loads(rspGetVacations.text)
    for vacation in jsonGetVacations:
        dictVacations[vacation['_id']] = vacation

def mergeResources2ResourceGroups(dictResources ,dictResourceGroups):
    for resourceGroup in dictResourceGroups.values():
        for resource in resourceGroup['resources']:
            if 'dictResources' not in resourceGroup.keys():
                resourceGroup['dictResources'] = [] if resource not in dictResources else [dictResources[resource]]

            if resource in dictResources.keys():
                resourceGroup['dictResources'].append(dictResources[resource])
            else:
                rspGetMissingResource = requests.get(f"{HUBPLANNER_ROOT_URL}resource/{resource}", headers=HUBPLANNER_HEADERS)
                jsonGetMissingResource = json.loads(rspGetMissingResource.text)
                if  'error' in jsonGetMissingResource.keys() and \
                        jsonGetMissingResource['error'] == 'entity.does.not.exist':
                        log.logger.warn(f'Unable to find ResourceID[{resource}] in dictResources for resourceGroupName[{resourceGroup["name"]}]')
                else:
                    if jsonGetMissingResource['status'] != 'STATUS_ARCHIVED':                        
                        if (jsonGetMissingResource['useCustomAvailability'] == False):
                            jsonGetMissingResource['customAvailabilities'] = {
                            'weekDays': {
                                            "monday": {
                                                "workDay": True,
                                                "minutes": 480
                                            },
                                            "tuesday": {
                                                "workDay": True,
                                                "minutes": 480
                                            },
                                            "wednesday": {
                                                "workDay": True,
                                                "minutes": 480
                                            },
                                            "thursday": {
                                                "workDay": True,
                                                "minutes": 480
                                            },
                                            "friday": {
                                                "workDay": True,
                                                "minutes": 480
                                            },
                                            "saturday": {
                                                "workDay": False,
                                                "minutes": 0
                                            },
                                            "sunday": {
                                                "workDay": False,
                                                "minutes": 0
                                            }
                                        },
                                    '_id' : 'default'
                                    }
                            totalHoursCapacity = 0
                            for weekDay in jsonGetMissingResource['customAvailabilities'].get('weekDays').values():
                                totalHoursCapacity = totalHoursCapacity + (weekDay['minutes'] / 60)
                            jsonGetMissingResource['totalHoursCapacity'] = totalHoursCapacity
                            jsonGetMissingResource['fullName'] = (jsonGetMissingResource['firstName'] + ' ' + jsonGetMissingResource['lastName']).strip()

                        if 'dictResources' not in resourceGroup.keys():
                            None
                        resourceGroup['dictResources'].append(jsonGetMissingResource)
                        dictResources[jsonGetMissingResource['_id']] = jsonGetMissingResource
                        #dictResources.get(jsonGetMissingResource['_id'])['fullName'] = dictResources.get(jsonGetMissingResource['_id'])['firstName'] + ' ' + dictResources.get(jsonGetMissingResource['_id'])['lastName']
    return dictResourceGroups
def mergeBookings2Resources(dictBookings, dictResources):
    for booking in dictBookings.values():
        if booking['resource'] in dictResources:
            resource = dictResources[booking['resource']]
            if 'bookings' not in resource.keys():
                resource['bookings'] = [booking]
            else:
                resource['bookings'].append(booking)
    return dictResources
def mergeProjects2Bookings(dictProjects, dictEvents, dictVacations, dictBookings):
    for booking in dictBookings.values():
        if booking['project'] in dictProjects.keys():
            booking['dictProject'] = dictProjects[booking['project']]
        elif booking['project'] in dictEvents.keys():
            booking['dictProject'] = dictEvents[booking['project']]
        elif booking['project'] in dictVacations.keys():
            booking['dictProject'] = dictVacations[booking['project']]
        else:
            log.logger.warning("Unable to find projectID[%s] in dictionaries for bookingID[%s]",
                        booking['project'], booking['_id'])
    return dictBookings
def getMergeOnResourceGroup(resourceGroupParams):
    # Init call
    tt.start()
    log.logger.info("Get Merge on ResourceGroups Called")
    t.start()


    # Get HubPlanner Data
    dictResourceGroups = getResourceGroups(resourceGroupParams)
    log.logger.info("Get Resource Groups Duration[%s]", str(t))
    t.start()

    dictResources = getActiveResources()
    log.logger.info("Get Resources Duration[%s]", str(t))
    t.start()

    dictBookings = getBookings()
    log.logger.info("Get Bookings Duration[%s]", str(t))
    t.start()

    dictProjects = getProjects()
    log.logger.info("Get Projects Duration[%s]", str(t))
    t.start()

    dictEvents = getEvents()
    log.logger.info("Get Events Duration[%s]", str(t))
    t.start()

    dictVacations = getVacations()
    log.logger.info("Get Vacations Duration[%s]", str(t))
    t.start()
    
    # Merge HubPlanner Data
    dictBookings = mergeProjects2Bookings(dictProjects, dictEvents, dictVacations, dictBookings)
    log.logger.info("Merge Projects into Bookings Duration[%s]", str(t))
    t.start()

    dictResources = mergeBookings2Resources(dictBookings, dictResources)
    log.logger.info("Merge Bookings into Resources Duration[%s]", str(t))
    t.start()

    dictResourceGroups = mergeResources2ResourceGroups(dictResources, dictResourceGroups)
    log.logger.info("Merge Resources into Resource Groups Duration[%s]", str(t))
    t.start()

    # Get missing unassigned/pipeline work data
    for resourceGroup in dictResourceGroups.values():
        if 'dictResources' in resourceGroup.keys():
            for resource in resourceGroup['dictResources']:
                if resource['firstName'].startswith('*'):
                    # is Unassigned resource
                    dictUnassignedBookings = getBookings({"resource": resource['_id']})
                    dictUnassignedBookings = mergeProjects2Bookings(dictProjects, dictEvents, dictVacations, dictUnassignedBookings)
                    dictResources = mergeBookings2Resources(dictUnassignedBookings, dictResources)
                    
    log.logger.info("Get and Merge missing unassigned/pipeline bookings Duration[%s]", str(t))
    t.start()

    
    # End Call
    log.logger.info("Get Merge on ResourceGroups Duration[%s]", str(tt))
    t.stop()
    tt.stop()
    return dictResourceGroups