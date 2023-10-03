import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db import connection,DatabaseError,IntegrityError,connections
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ast import Continue
from asyncio.windows_events import NULL
import datetime
from datetime import date, datetime, timedelta
from stopwatch import Stopwatch
from dateutil import tz

from hubplanner.models import Bookings, Person, Project
from . import hubplannerdata
from logger.logger import LoggerView
from estimating.models import Departmentalforcatsedhour, Projectdetail
from estimating.serializers import DepartmentalforcatsedhourSerializer
from django.core import serializers
from rest_framework.generics import ListAPIView
from .utils.helper import DepartmentalHours, ProjectDepartmentalHours
import re

@api_view()
def importHubplannerData (request):

    RESOURCE_GROUP_PARAMETERS = [
            {
                'deptName': 'LPS Electrical Design',
                '_ids':['5f1ee734f3a6d50b490bb1d9']
            },
            {
                'deptName': 'LPS Controls Engineering',
                '_ids':['5f1ee728f3a6d50b490bb140']
            },
            {
                'deptName': 'LPS Mechanical Design Engineering',
                '_ids': ['5f1ee757e445f70b4ac26110']        
            },
            {
                'deptName': 'LPS Mechanical Project Engineering',
                '_ids': ['6226537a48a2e20c7c77dde4']
            },
            # {
            # {
            #     'deptName': "D+F GLobal Ops Software Product Development",
            #     '_ids': ['61e07cd86d26140c40d4d81c']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Solution Integration",
            #     '_ids': ['63ffb44ccbd2ee0b8ea4bac8']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Delivery",
            #     '_ids': ['6434685e4674900be3a791b4']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Implementation and Infrastructure",
            #     '_ids': ['6434687c4674900be3a79296']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Project Manager",
            #     '_ids': ['64778f926b84bf0ca978f8d8']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Developers",
            #     '_ids': ['64778fb3c84f7a0c92227958']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Product Management",
            #     '_ids': ['648b5e8eeb07200c48c05f55']
            # },
            # {
            #     'deptName': "D+F Global Ops Software QA",
            #     '_ids': ['648b65134afea30c3f953a18']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Program Manager",
            #     '_ids': ['648b65524afea30c3f953b6c']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Scrum Master",
            #     '_ids': ['648b659beb07200c48c08d7a']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Integration Management",
            #     '_ids': ['648b65ceeb07200c48c0917d']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Commisioning Engineer",
            #     '_ids': ['648b663b4afea30c3f954256']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Solution Architect",
            #     '_ids': ['648b667229bb5e0c4004dc07']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Delivery Engineer",
            #     '_ids': ['648b6b1e29bb5e0c4004ebbe']
            # },
            # {
            #     'deptName': "D+F Global Ops Software Platform Engineering",
            #     '_ids': ['6492130960ddbe0c55259cd3']
            # },
            # {
            #     'deptName': "D+F GLOBAL OPS SOFTWARE PROJECT LEADS",
            #     '_ids': ['64ac60b80ca2c50c52c6b230']
            # },

            # {
            #     'deptName': "D+F Global Ops Software Architects",
            #     '_ids': ['64ac62b715e0fc0c4adcd33d']
            # },


            # {
            #     'deptName': "D+F Global Ops Software WCS",
            #     '_ids': ['64d3d41cdc6ad2211cb2b0f2']
            # },
            # {
            #     'deptName': "D+F Global Ops WCS Software Development R&D",
            #     '_ids': ['64e36e8e93584119d8ee364a']
            # }
            ]

    # create and start stopwatches
    # t = incremental stopwatch
    # tt = full script stopwatch
    t = Stopwatch()
    tt = Stopwatch()
    t.start()
    tt.start()

    # init and get the logger
    log = LoggerView(log_file='log.log')
    log.logger.info("Script Started logger Init Duration[%s]", str(t))
    t.start()

    # Script Code
    try:
        today = datetime.today()
        #today = datetime.today() + timedelta(days=-10)

        currentWeekStart = today- timedelta(days=today.weekday()+1)
        lastWeekStart = currentWeekStart - timedelta(days=7)
        futureWeek4Start = currentWeekStart + timedelta(days=21)
        futureWeek12Start = currentWeekStart + timedelta(days=77)

        currentWeekEnd = currentWeekStart + timedelta(days=6)
        lastWeekEnd = lastWeekStart + timedelta(days=6)
        futureWeek4End = futureWeek4Start + timedelta(days=6)
        futureWeek12End = futureWeek12Start + timedelta(days=6)

        dictResourceGroups = hubplannerdata.getMergeOnResourceGroup(RESOURCE_GROUP_PARAMETERS)

        # Get all bookings between 1 week in the past and 12 weeks in the future
        # and seperate them into by day booking records
        # ignore Not Available Bookings
        bookingDays = []
        bookingsMap = {}
        for resourceGroup in dictResourceGroups.values():
            if 'dictResources' in resourceGroup.keys():
                for resource in resourceGroup['dictResources']:
                    if 'bookings' in resource.keys():
                        for booking in resource['bookings']:  
                            
                            # is this booking entirely in the past? If so, skip it
                            if (booking['start'] < lastWeekStart) \
                                and booking['end'] < lastWeekStart:
                                continue

                            # is this booking entirely in the future? If so, skip it
                            if (booking['start'] > futureWeek12End):
                                continue

                            if 'dictProject' in booking.keys():
                                project = booking['dictProject']

                                # ignore Not Available Bookings
                                if project['name'] == 'Not Available' \
                                    or ('status' in project.keys() and project['status'] == 'STATUS_ARCHIVED'):
                                    continue

                                # get count of days in the booking for seperating booking hours by day
                                countDays = 0
                                whileLoopDate = booking['start']
                                while whileLoopDate <= booking['end']:
                                    dayAvailability = resource['customAvailabilities'].get('weekDays').get(whileLoopDate.strftime('%A').lower())
                                    if dayAvailability['workDay'] == True:
                                        countDays = countDays + 1
                                    whileLoopDate = whileLoopDate + timedelta(days=1)

                                # only count the days of the booking in the current timeframe
                                if booking['start'] < lastWeekStart:
                                    whileLoopDate = lastWeekStart
                                else:
                                    whileLoopDate = booking['start']

                                # get the booking hours per day and add the booking by day record to the list and map
                                while whileLoopDate <= futureWeek12End \
                                    and whileLoopDate <= booking['end']:
                                    dayAvailability = resource['customAvailabilities'].get('weekDays').get(whileLoopDate.strftime('%A').lower())
                                    if dayAvailability['workDay'] == True:
                                        match booking['state']:
                                            case 'STATE_TOTAL_MINUTE':
                                                minutes = round(booking['stateValue'] / countDays)
                                                allocationType = 'Total Hours'
                                            case 'STATE_PERCENTAGE':
                                                minutes = round((booking['stateValue'] / 100) * dayAvailability['minutes'])
                                                allocationType = 'Percentage'
                                            case 'STATE_DAY_MINUTE':
                                                minutes = round(booking['stateValue'])
                                                allocationType = 'Hours/Day'
                                        
                                        if 'projectCode' in project.keys():
                                            projectNum = project['projectCode']
                                            projectStatus = project['status']
                                        else:
                                            # change Vacation events to PTO to match other sources of data
                                            if project['name'] == 'Vacation':
                                                projectNum = 'PTO'
                                            else:
                                                projectNum =  project['name']
                                            projectStatus = 'STATUS_ACTIVE'

                                        # create the booking day record and add to the master list
                                        bookingDay = {
                                            'Employee' : resource['fullName'],
                                            'ProjectNum' : projectNum,
                                            'ProjectName' : project['name'],
                                            'date' : whileLoopDate,
                                            'hours' : minutes/60,
                                            'allocationType' : allocationType,
                                            'category' : booking['categoryName'],
                                            'weeklyCapacity': resource['totalHoursCapacity'],
                                            'projectStatus' : projectStatus,
                                            'hubPlannerId' : resource['_id'],
                                            'resourceGroupName': resourceGroup['name'],
                                            'hubPlannerResourceGroupId' : resourceGroup['_id']
                                        }
                                        bookingDays.append(bookingDay.copy())
                                
                                        # add the booking to the map of bookings
                                        if booking['_id'] not in bookingsMap.keys():
                                            bookingsMap[booking['_id']] = bookingDay.copy()

                                    # increment to next day in while loop
                                    whileLoopDate = whileLoopDate + timedelta(days=1)     
                            else:
                                None          
                    else:
                        log.logger.warning("No bookings for Resource[%s] in HubPlaner",
                            resource['fullName'])
            else:
                None

        # Summarize the by day data by week
        resourceWeeklyMap = {}
        projectWeeklyMap = {}
        projectResourceWeeklyMap = {}
        for bookingDay in bookingDays:
            currentBookingWS = bookingDay['date'] - timedelta(days=bookingDay['date'].weekday() + 1)
            currentBookingWSText = currentBookingWS.strftime('%m/%d/%Y')

            resourceWeeklyKey = bookingDay['Employee'] + " " + currentBookingWSText
            projectWeeklyKey = bookingDay['ProjectNum'] + " " + currentBookingWSText
            projectResourceWeeklyKey = bookingDay['Employee'] + " " + bookingDay['ProjectNum'] + " " + currentBookingWSText

            if resourceWeeklyKey in resourceWeeklyMap.keys():
                resourceWeeklyMap.get(resourceWeeklyKey)['bookedHours'] = resourceWeeklyMap.get(resourceWeeklyKey)['bookedHours'] + bookingDay['hours']
            else:
                resourceWeeklyMap[resourceWeeklyKey] = {
                    'Employee': bookingDay['Employee'],
                    'date': currentBookingWSText,
                    'bookedHours': bookingDay['hours'],
                    'capacityHours': bookingDay['weeklyCapacity'],
                    'hubPlannerId' : bookingDay['hubPlannerId'],
                    'resourceGroupName' : bookingDay['resourceGroupName'],
                    'hubPlannerResourceGroupId' : bookingDay['hubPlannerResourceGroupId']
                }

            if projectWeeklyKey in projectWeeklyMap.keys():
                projectWeeklyMap.get(projectWeeklyKey)['bookedHours'] = projectWeeklyMap.get(projectWeeklyKey)['bookedHours'] + bookingDay['hours']
            else:
                projectWeeklyMap[projectWeeklyKey] = {
                    'ProjectNum': bookingDay['ProjectNum'],
                    'ProjectName': bookingDay['ProjectName'],
                    'date': currentBookingWSText,
                    'bookedHours': bookingDay['hours'],
                    'projectStatus': bookingDay['projectStatus']
                }

            if projectResourceWeeklyKey in projectResourceWeeklyMap.keys():
                projectResourceWeeklyMap.get(projectResourceWeeklyKey)['bookedHours'] = projectResourceWeeklyMap.get(projectResourceWeeklyKey)['bookedHours'] + bookingDay['hours']
            else:
                projectResourceWeeklyMap[projectResourceWeeklyKey] = {
                    'Employee': bookingDay['Employee'],
                    'ProjectNum': bookingDay['ProjectNum'],
                    'ProjectName' : bookingDay['ProjectName'],
                    'date': currentBookingWSText,
                    'bookedHours': bookingDay['hours'],
                    'projectStatus': bookingDay['projectStatus'],
                    'category' : bookingDay['category'],
                    'resourceGroupName' : bookingDay['resourceGroupName'],
                    # 'hubPlannerResourceGroupId' : bookingDay['hubPlannerResourceGroupId']
                }

        # Fill in each week for each resource if there 
        # where no bookings at all in that week
        unallocatedWeeklyMap = {}
        whileLoopDate = lastWeekStart
        while whileLoopDate <= futureWeek12End:
            for resourceGroup in dictResourceGroups.values():
                if 'dictResources' in resourceGroup.keys():
                    for resource in resourceGroup['dictResources']:
                        if 'fullName' in resource.keys():
                            resourceWeeklyKey = resource['fullName'] + " " + whileLoopDate.strftime('%m/%d/%Y')
                            if resourceWeeklyKey not in resourceWeeklyMap.keys():
                                resourceWeeklyMap[resourceWeeklyKey] = {
                                    'Employee': resource['fullName'],
                                    'date': whileLoopDate.strftime('%m/%d/%Y'),
                                    'bookedHours': 0,
                                    'capacityHours': resource['totalHoursCapacity'],
                                    'hubPlannerId' : resource['_id'],
                                    'resourceGroupName' : resourceGroup['name'],
                                    'hubPlannerResourceGroupId' : resourceGroup['_id'],
                                }
                                unallocatedWeeklyMap[resourceWeeklyKey] = resourceWeeklyMap[resourceWeeklyKey]                         

            whileLoopDate = whileLoopDate + timedelta(days=7)

        # Create Unallocated bookings to capture difference 
        # between booked hours and capacity hours
        for resourceWeeklyKey, resourceWeekly in resourceWeeklyMap.items():
            if resourceWeekly['bookedHours'] < resourceWeekly['capacityHours']:
                resourceWeekly['unallocatedHours'] = resourceWeekly['capacityHours'] - resourceWeekly['bookedHours']
                unallocatedWeeklyMap[resourceWeeklyKey] = resourceWeekly
            else:
                resourceWeekly['unallocatedHours'] = 0
            
            if resourceWeekly['capacityHours'] != 0:
                resourceWeekly['percentUtilization'] = resourceWeekly['bookedHours'] / resourceWeekly['capacityHours']
            else:
                resourceWeekly['percentUtilization'] = 1

            if resourceWeekly['Employee'].startswith('*'):
                resourceWeekly['percentUtilization'] = 1
                resourceWeekly['unallocatedHours'] = 0
                resourceWeekly['capacityHours'] = 0
                

        # add the unallocated weekly hours to the Resource and Project Map
        for unallocatedWeekly in unallocatedWeeklyMap.values():
            if unallocatedWeekly['Employee'].startswith('*'):
                Continue
            projectResourceWeeklyKey = unallocatedWeekly['Employee'] + ' ' + 'Unallocated' + ' ' + unallocatedWeekly['date']
            projectResourceWeeklyMap[projectResourceWeeklyKey] = {
                    'Employee': unallocatedWeekly['Employee'],
                    'ProjectNum': 'Unallocated',
                    'date': unallocatedWeekly['date'],
                    'bookedHours': unallocatedWeekly['unallocatedHours'],
                    'projectStatus': 'STATUS_UNALLOCATED',
                    'resourceGroupName' : unallocatedWeekly['resourceGroupName'],
                    # 'hubPlannerResourceGroupId' : unallocatedWeekly['hubPlannerResourceGroupId']

                }

        with connection.cursor() as cursor:
            # Resources By Week Sheet
            for record in resourceWeeklyMap.values():
                try: 
                    query = 'exec AddResourcesByWeek %s, %s, %s, %s, %s, %s, %s, %s, %s'
                    args = (record['Employee'],record['date'],format(record['bookedHours'],'.2f'),format(record['capacityHours'],'.2f'),format(record['unallocatedHours'],'.2f'),format(record['percentUtilization'],'.2f'),record['hubPlannerId'],record['resourceGroupName'],record['hubPlannerResourceGroupId'])
                    cursor.execute(query, args)
                    # cursor.execute("exec AddResourcesByWeek @employee = ?, @Weekstartdate = ?, @bookedHours =?, @capacityHours=?,@unAllocatedHours=?,@percentUtilization=?,@hubPlannerId=?",record['Employee'],record['date'],format(record['bookedHours'],'.2f'),format(record['capacityHours'],'.2f'),format(record['unallocatedHours'],'.2f'),format(record['percentUtilization'],'.2f'),record['hubPlannerId'])
                except IntegrityError as err:
                    log.logger.info("some data that violates the integrity of the database while adding Resources By week : [%s] [%s]",record['Employee'],record['date'])
                # except KeyError as err:
                #     logger.info("Resource :[%s] [%s]",record['Employee'],record['date'])
            cursor.commit()
            
            # Projects By Week Sheet

            for record in projectWeeklyMap.values():
                try:   
                    query = 'exec AddProjectsByWeek %s, %s, %s, %s'
                    args = (record['ProjectNum'],record['date'],format(record['bookedHours'],'.2f'),record['projectStatus'])
                    cursor.execute(query, args)
                    # cursor.execute("exec AddProjectsByWeek @projectNumber = ?, @Weekstartdate = ?, @bookedHours =?, @status=?",record['ProjectNum'],record['date'],format(record['bookedHours'],'.2f'),record['projectStatus'])
                except IntegrityError as err:
                    log.logger.info("some data that violates the integrity of the database while adding Projects By week: [%s] [%s]",record['projectNumber'],record['date'])

            cursor.commit()
            # Projects & Employees Week Sheet
            for record in projectResourceWeeklyMap.values():
                try:   
                    category =''
                    if 'category' in record:
                        category = record['category']
                        # cursor.execute("exec AddProjectsEmployeesByWeek @employeeName = ?, @projectNumber = ?, @Weekstartdate = ?, @bookedHours = ?, @status = ?, @bookingCategory = ? ",record['Employee'], record['ProjectNum'],record['date'],format(record['bookedHours'],'.2f'),record['projectStatus'],record['category'])
                    else:
                        category = 'Unallocated'
                        # cursor.execute("exec AddProjectsEmployeesByWeek @employeeName = ?, @projectNumber = ?, @Weekstartdate = ?, @bookedHours = ?, @status = ?, @bookingCategory = 'Unallocated'",record['Employee'], record['ProjectNum'],record['date'],format(record['bookedHours'],'.2f'),record['projectStatus'])
                    query = 'exec AddProjectsEmployeesByWeek %s, %s, %s, %s, %s, %s'
                    args = (record['Employee'], record['ProjectNum'],record['date'],format(record['bookedHours'],'.2f'),record['projectStatus'],category)
                    cursor.execute(query, args)
                except IntegrityError as err:
                    log.logger.info("some data that violates the integrity of the database while adding Projects and  Employees By week: [%s] [%s] [%s]",record['Employee'], record['projectNumber'],record['date'])

            cursor.commit()

            log.logger.info("Script Finished Total Duration[%s]", str(tt))
    except:
        log.logger.exception("Main exception")
    return Response("Hubplanner ok!")

# @api_view()
# def updateDepartmentalHoursToHubplanner(request):
#     log = LoggerView(log_file='log.log')
#     # log.logger.info("Script Started logger Init Duration[%s]", str(t))
#     resourceId = '640e6cc6df9d4b0b98a18ecc'
#     projectId = '64c00620604e3d0c7e9ccfd7'
#     startDate = '2023-07-30'
#     endDate = '2023-08-19'
#     allDay = "false"
#     state = "STATE_TOTAL_MINUTE"
#     totalHour = 400
#     stateValue = totalHour * 60
#     url = 'https://api.hubplanner.com/v1/booking'
#     method  = 'POST'
#     bodyData = '{"resource":"'+resourceId+'","start":"'+startDate+'","end":"'+endDate+'","project":"'+projectId+'","allDay":'+allDay+',"state":"'+state+'","stateValue":'+str(stateValue)+'}'
#     returnValue = ''
#     print(bodyData)
#     with connection.cursor() as cursor:
#         try:
#             query = 'exec AddProjectToHubplanner %s, %s, %s, %s'
#             args = (url,method,bodyData,returnValue)
#             cursor.execute(query, args)
#         except Exception as err:
#             log.logger.error("updateDepartmentalHorsToHubplanner Error :[%s] [%s] [%s]",err, resourceId,projectId)
#         cursor.commit()
#     return Response('Hubplanner Hours Updated!')
def createClientToHubplanner(customer,projectId):
    hubplannerClientList = hubplannerdata.getClients()
    pattern = re.compile(r'\b' + str(customer) + r'\b')
    clientID = next((k for k, v in hubplannerClientList.items() if pattern.search(str(v))), None)
    if(clientID is None and customer is not NULL):
        database = 'ProjectDB'
        log = LoggerView(log_file='log.log')
        url = 'https://api.hubplanner.com/v1/client'
        method  = 'POST'
        bodyData = '{"name":"'+str(customer)+'"}'
        print("Create Client BodyData",str(bodyData))
        with connections[database].cursor() as cursor:
            try:
                query = 'DECLARE @ReturnValue nvarchar(max);exec AddProjectToHubplanner %s, %s, %s, @ReturnValue OUTPUT;Select @ReturnValue;'
                args = (url,method,bodyData)
                # returnId = cursor.execute(query, args).fetchval()
                # print('returnId: ',returnId)
                cursor.execute(query, args)
                row = cursor.fetchone()
                print("add row: ",row)
                if row:
                    data = json.loads(row[0])
                    # Access the _id field
                    clientID = data["_id"]
                # addOrUpdateBookings(projectDepartmentalHours)
            except Exception as err:
                log.logger.error("createClientToHubplanner Error :[%s] [%s]",err, customer)
            cursor.commit()
        # attachClientToHubplannerProject(clientID,projectId)
    # return projectDepartmentalHours
    return clientID

def attachClientToHubplannerProject(clientID,projectId):
    if(clientID is not None and projectId is not None):
        database = 'ProjectDB'
        log = LoggerView(log_file='log.log')
        url = 'https://api.hubplanner.com/v1/project/'+projectId+'/client'
        method  = 'POST'
        bodyData = '"clientIds":["'+clientID+'"]}'
        print("Create Client BodyData",str(bodyData))
        with connections[database].cursor() as cursor:
            try:
                query = 'DECLARE @ReturnValue nvarchar(max);exec AddProjectToHubplanner %s, %s, %s, @ReturnValue OUTPUT;Select @ReturnValue;'
                args = (url,method,bodyData)
                # returnId = cursor.execute(query, args).fetchval()
                # print('returnId: ',returnId)
                cursor.execute(query, args)
                row = cursor.fetchone()
                print("add row: ",row)
                if row:
                    data = json.loads(row[0])
                    # Access the _id field
                    clientID = data["_id"]
                # addOrUpdateBookings(projectDepartmentalHours)
            except Exception as err:
                log.logger.error("attachClientToHubplannerProject Error :[%s] [%s] [%s]",err, clientID, projectId)
            cursor.commit()
    # return projectDepartmentalHours

def createPendingProjectToHubplanner(projectNumber,customer):
    database = 'ProjectDB'
    log = LoggerView(log_file='log.log')
    
    url = 'https://api.hubplanner.com/v1/project'
    method  = 'POST'
    bodyData = '{"name":"'+projectNumber+'","projectCode":"'+projectNumber+'","status":"STATUS_PENDING"}'
    projectId = ''
    print("Create Pending Project BodyData",str(bodyData))
    
    with connections[database].cursor() as cursor:
        try:
            query = 'DECLARE @ReturnValue nvarchar(max);exec AddProjectToHubplanner %s, %s, %s, @ReturnValue OUTPUT;Select @ReturnValue;'
            args = (url,method,bodyData)
            # returnId = cursor.execute(query, args).fetchval()
            # print('returnId: ',returnId)
            cursor.execute(query, args)
            row = cursor.fetchone()
            print("add row: ",row)
            if row:
                data = json.loads(row[0])
                # Access the _id field
                projectId = data["_id"]
                clientID = createClientToHubplanner(customer,projectId)
            # addOrUpdateBookings(projectDepartmentalHours)
        except Exception as err:
            log.logger.error("createPendingProjectToHubplanner Error :[%s] [%s]",err, projectNumber)
        cursor.commit()
    # return projectDepartmentalHours
    return projectId

def addDepartmentalHoursToHubplanner(projectDepartmentalHours):
    database = 'ProjectDB'
    log = LoggerView(log_file='log.log')
    allDay = "false"
    state = "STATE_TOTAL_MINUTE"
    url = 'https://api.hubplanner.com/v1/booking'
    method  = 'POST'
    bodyData = '{"resource":"'+projectDepartmentalHours.resourceId+'","start":"'+projectDepartmentalHours.startDate+'","end":"'+projectDepartmentalHours.endDate+'","project":"'+projectDepartmentalHours.projectId+'","allDay":'+allDay+',"state":"'+state+'","stateValue":'+str(projectDepartmentalHours.stateValue)+'}'
    bookingId = ''
    print("Add Departmental Hours BodyData",str(bodyData))
    with connections[database].cursor() as cursor:
        try:
            query = 'DECLARE @ReturnValue nvarchar(max);exec AddProjectToHubplanner %s, %s, %s, @ReturnValue OUTPUT;Select @ReturnValue;'
            args = (url,method,bodyData)
            # returnId = cursor.execute(query, args).fetchval()
            # print('returnId: ',returnId)
            cursor.execute(query, args)
            row = cursor.fetchone()
            # print("add row: ",row)
            if row:
                data = json.loads(row[0])
                # Access the _id field
                bookingId = data["_id"]
            # addOrUpdateBookings(projectDepartmentalHours)
        except Exception as err:
            log.logger.error("addDepartmentalHorsToHubplanner Error :[%s] [%s] [%s]",err, projectDepartmentalHours.resourceId,projectDepartmentalHours.projectId)
        cursor.commit()
    # return projectDepartmentalHours
    return bookingId

def updateDepartmentalHoursToHubplanner(booking):
    database = 'ProjectDB'
    log = LoggerView(log_file='log.log')
    allDay = "false"
    state = "STATE_TOTAL_MINUTE"
    url = 'https://api.hubplanner.com/v1/booking/'+booking.bookingId
    method  = 'POST'
    bodyData = '{"resource":"'+booking.hubplannerResourceId+'","start":"'+booking.startDate+'","end":"'+booking.endDate+'","project":"'+booking.hubplannerProjectId+'","allDay":'+allDay+',"state":"'+state+'","stateValue":'+str(booking.stateValue)+'}'
    returnValue = ''
    print("Update Departmental Hours BodyData", str(bodyData))
    print("Booking ID: ",booking.bookingId)
    with connections[database].cursor() as cursor:
        try:
            query = 'exec AddProjectToHubplanner %s, %s, %s, %s'
            args = (url,method,bodyData,returnValue)
            cursor.execute(query, args)
            # addOrUpdateBookings(projectDepartmentalHours)
        except Exception as err:
            log.logger.error("updateDepartmentalHorsToHubplanner Error :[%s] [%s] [%s]",err, booking.hubplannerResourceId,booking.hubplannerProjectId)
        cursor.commit()
        
def addOrUpdateBookings(projectDepartmentalHours):
    log = LoggerView(log_file='log.log')
    tempBooking = Bookings.objects.using("ProjectDB").filter(hubplannerProjectId = projectDepartmentalHours.projectId, hubplannerResourceId = projectDepartmentalHours.resourceId, startDate = projectDepartmentalHours.startDate, endDate = projectDepartmentalHours.endDate, isDelete =False).first()
    print("tempBooking : ",tempBooking)
    if(tempBooking is None or tempBooking is NULL):
        nBooking = Bookings()
        try:
            print("addDepartmentalHoursToHubplanner : ")
            nBooking.bookingId = addDepartmentalHoursToHubplanner(projectDepartmentalHours)
            nBooking.hubplannerProjectId = projectDepartmentalHours.projectId
            nBooking.hubplannerResourceId = projectDepartmentalHours.resourceId
            nBooking.startDate = projectDepartmentalHours.startDate
            nBooking.endDate = projectDepartmentalHours.endDate
            nBooking.totalHour = projectDepartmentalHours.totalHour
            nBooking.stateValue = projectDepartmentalHours.stateValue
            # nBooking.projectId = Project.objects.using("ProjectDB").filter(hubplannerprojectid = projectDepartmentalHours.projectId).first()
            # nBooking.personId = Person.objects.using("ProjectDB").filter(hubplannerid = projectDepartmentalHours.resourceId).first()
            nBooking.createdDate = datetime.now()
            nBooking.save(using='ProjectDB')
        except Exception as err:
            log.logger.error("addBookings Error: [%s] [%s] [%s]",err,projectDepartmentalHours.projectId,projectDepartmentalHours.resourceId)
       
    else:
        try:
            print("updateDepartmentalHoursToHubplanner : ")
            tempBooking.startDate = projectDepartmentalHours.startDate
            tempBooking.endDate = projectDepartmentalHours.endDate
            tempBooking.totalHour = projectDepartmentalHours.totalHour
            tempBooking.stateValue = projectDepartmentalHours.stateValue
            # tempBooking.projectId = Project.objects.using("ProjectDB").filter(hubplannerprojectid = projectDepartmentalHours.projectId).first()
            # tempBooking.personId = Person.objects.using("ProjectDB").filter(hubplannerid = projectDepartmentalHours.resourceId).first()
            tempBooking.save(using='ProjectDB')
            updateDepartmentalHoursToHubplanner(tempBooking)
        except Exception as err:
            log.logger.error("updateBookings Error: [%s] [%s] [%s]",err,tempBooking.hubplannerResourceId,tempBooking.hubplannerProjectId)

@api_view()
def getDepartmentalHoursToHubplanner(request):
    queryset = Departmentalforcatsedhour.objects.using("EstimatingDB").all()
    list_of_items = list(queryset)
    # result = serializers.serialize('json', queryset)
    serializer = DepartmentalforcatsedhourSerializer( list_of_items,many=True)
   
    # if serializer.is_valid() :
    #     print("data: ")
    #     print(serializer.data)
    # else:
    #     print("Error: ")
    #     print(serializer.errors)

    return Response(serializer.data)

# class getDepartmentalHoursToHubplanner(ListAPIView):
#      result = Departmentalforcatsedhour.objects.using("EstimatingDB").all()
#      projectList = Departmentalforcatsedhour.objects.using("EstimatingDB").values_list('projectnumber')
#      print(projectList)
#      queryset = list(result)
#      print(queryset)

#      serializer_class = DepartmentalforcatsedhourSerializer
#      print(serializer_class.data)

@api_view()
def addOrUpdateDepartmentalHoursToHubplanner(request):
    departmentalHours = DepartmentalHours.departmentalHours_list()
    # print(departmentalHours)
    queryset = Departmentalforcatsedhour.objects.select_related('projectdetailid').using("EstimatingDB").all()
    # print(queryset)
    list_of_items = list(queryset)
    # print(list_of_items.__getitem__(0))
    # list_of_dicts = [item.to_dict() for item in list_of_items]

    # print(type(list(queryset)))
    # print(list(queryset))
    # result = serializers.serialize('json', queryset)
    serializer = DepartmentalforcatsedhourSerializer( list_of_items,many=True)
    projectList = Departmentalforcatsedhour.objects.using("EstimatingDB").values_list('projectnumber',flat=True).distinct()
    # projectList = Projectdetail.objects.using("EstimatingDB").values_list('projectnumber',flat=True).distinct()
    print(projectList)
    hubplannerProjectList = hubplannerdata.getProjects()
    print(hubplannerProjectList.get('64d2a9220065e319de5a68f6'))
    for item in projectList:
        # if(hubplannerProjectList.items.__name__ == item):
        # projectID = [k for k, v in hubplannerProjectList.items() if v.__name__ == item][0]
        # value = 'name' :
        projectNumberPattern = re.compile(r'\b' + str(item) + r'\b')
        projectStatusPattern = re.compile(r'\b' + 'STATUS_ARCHIVED' + r'\b')
        projectID = next((k for k, v in hubplannerProjectList.items() if projectNumberPattern.search(str(v)) and not projectStatusPattern.search(str(v))), None)
        print(projectID)
        print(item)
        customer = queryset.filter(projectnumber=item).order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('projectdetailid__customer', flat=True)[0]
        EE = DepartmentalHours.get_object_with_code(departmentalHours,'EE')
        print(EE.departmentName)
        # print(queryset.filter(projectnumber=item, description='ELEC PROJ ENG - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='ELEC PROJ ENG - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True))
        EE.hours = queryset.filter(projectnumber=item, description='ELEC PROJ ENG - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='ELEC PROJ ENG - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        print(EE.hours)
        if(EE.hours > 0):
            if(projectID != None):
                EEObject = ProjectDepartmentalHours(projectId=projectID,resourceId=EE.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=EE.hours,stateValue=EE.hours*60)
                addOrUpdateBookings(EEObject)
            else:
                projectID = createPendingProjectToHubplanner(item,customer)
                EEObject = ProjectDepartmentalHours(projectId=projectID,resourceId=EE.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=EE.hours,stateValue=EE.hours*60)
                addOrUpdateBookings(EEObject)

        ED = DepartmentalHours.get_object_with_code(departmentalHours,'ED')
        ED.hours = queryset.filter(projectnumber=item, description='ELEC DESIGN - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='ELEC DESIGN - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        print(ED.hours)
        if(ED.hours > 0):
            if(projectID != None):
                EDObject = ProjectDepartmentalHours(projectId=projectID,resourceId=ED.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=ED.hours,stateValue=ED.hours*60)
                addOrUpdateBookings(EDObject)
            else:
                projectID = createPendingProjectToHubplanner(item,customer)
                EDObject = ProjectDepartmentalHours(projectId=projectID,resourceId=ED.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=ED.hours,stateValue=ED.hours*60)
                addOrUpdateBookings(EDObject)

        CEP = DepartmentalHours.get_object_with_code(departmentalHours,'CEP')
        CEP.hours = queryset.filter(projectnumber=item, description='ELEC DESIGN - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='ELEC DESIGN - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        print(CEP.hours)
        if(CEP.hours > 0):
            if(projectID != None):
                CEPObject = ProjectDepartmentalHours(projectId=projectID,resourceId=CEP.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=CEP.hours,stateValue=CEP.hours*60)
                addOrUpdateBookings(CEPObject)
            else:
                projectID = createPendingProjectToHubplanner(item,customer)
                CEPObject = ProjectDepartmentalHours(projectId=projectID,resourceId=CEP.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=CEP.hours,stateValue=CEP.hours*60)
                addOrUpdateBookings(CEPObject)
            
        CED = DepartmentalHours.get_object_with_code(departmentalHours,'CED')
        CED.hours = queryset.filter(projectnumber=item, description='ELEC DESIGN - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='ELEC DESIGN - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        print(CED.hours)
        if(CED.hours > 0):
            if(projectID != None):
                CEDObject = ProjectDepartmentalHours(projectId=projectID,resourceId=CED.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=CED.hours,stateValue=CED.hours*60)
                addOrUpdateBookings(CEDObject)
            else:
                projectID = createPendingProjectToHubplanner(item,customer)
                CEDObject = ProjectDepartmentalHours(projectId=projectID,resourceId=CED.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=CED.hours,stateValue=CED.hours*60)
                addOrUpdateBookings(CEDObject)
            

        ME = DepartmentalHours.get_object_with_code(departmentalHours,'ME')
        ME.hours = queryset.filter(projectnumber=item, description='MECH PROJ ENG - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='MECH PROJ ENG - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        print(ME.hours)
        if(ME.hours > 0):
            if(projectID != None):
                MEObject = ProjectDepartmentalHours(projectId=projectID,resourceId=ME.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=ME.hours,stateValue=ME.hours*60)
                addOrUpdateBookings(MEObject)
            else:
                projectID = createPendingProjectToHubplanner(item,customer)
                MEObject = ProjectDepartmentalHours(projectId=projectID,resourceId=ME.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=ME.hours,stateValue=ME.hours*60)
                addOrUpdateBookings(MEObject)
            

        MD = DepartmentalHours.get_object_with_code(departmentalHours,'MD')
        MD.hours = queryset.filter(projectnumber=item, description='MECH DESIGN - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='MECH DESIGN - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        print(MD.hours)
        if(MD.hours > 0):
            if(projectID != None):
                MDObject = ProjectDepartmentalHours(projectId=projectID,resourceId=MD.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=MD.hours,stateValue=MD.hours*60)
                addOrUpdateBookings(MDObject)
            else:
                projectID = createPendingProjectToHubplanner(item,customer)
                MDObject = ProjectDepartmentalHours(projectId=projectID,resourceId=MD.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=MD.hours,stateValue=MD.hours*60)
                addOrUpdateBookings(MDObject)
        
        # SE = DepartmentalHours.get_object_with_code(departmentalHours,'SE')
        # SE.hours = queryset.filter(projectnumber=item, description='MECH DESIGN - ST').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0] + queryset.filter(projectnumber=item, description='MECH DESIGN - OT').order_by('-projectdetailid__revisionnumber', '-projectdetailid__baseversion', '-projectdetailid__optionversion').values_list('quantity', flat=True)[0]
        # print(SE.hours)
        # if(SE.hours > 0):
        #     if(projectID != None):
        #         SEObject = ProjectDepartmentalHours(projectId=projectID,resourceId=SE.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=SE.hours,stateValue=SE.hours*60)
        #         addOrUpdateBookings(SEObject)
        #     else:
        #         projectID = createPendingProjectToHubplanner(item,customer)
        #         SEObject = ProjectDepartmentalHours(projectId=projectID,resourceId=SE.resourceId,startDate='2023-09-01',endDate='2023-09-30',totalHour=SE.hours,stateValue=SE.hours*60)
        #         addOrUpdateBookings(SEObject)
            
        pass
    # if serializer.is_valid() :
    #     print("data: ")
    #     print(serializer.data)
    # else:
    #     print("Error: ")
    #     print(serializer.errors)

    return Response(serializer.data)