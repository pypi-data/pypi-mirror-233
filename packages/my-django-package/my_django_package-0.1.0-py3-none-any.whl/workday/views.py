from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from pandas.tseries.frequencies import to_offset
from datetime import datetime
from logger.logger import LoggerView
import re

@api_view()
def importWorkdayData (request):
    log = LoggerView(log_file='log.log')
    log.logger.info('Import All Worker Time logs Table to DB.')

    try:

    # Import All Worker Time logs Table to DB
        # TAAOrganizationTime =  pd.read_excel("C:\\Users\\neha.yargal\\Documents\\LPS\\Data\\projectList.xlsx")
        TAAOrganizationTime =  pd.read_csv("C:\\Users\\neha.yargal\\Documents\\LPS\\WorkDayData\\TAAData\\TAAOrganizationTime.csv",parse_dates=['Date'],skiprows=5)
        TAAOrganizationTime['Date'] = pd.to_datetime(TAAOrganizationTime['Date'])
        TAATimeOff = pd.read_csv("C:\\Users\\neha.yargal\\Documents\\LPS\\WorkDayData\\TAAData\\TAATimeOff.csv", parse_dates=['Time Off Date'],skipfooter=1,skiprows=6)
        TAATimeOff['Time Off Date'] = pd.to_datetime(TAATimeOff['Time Off Date'])
        TAA_Holiday_Calendar = pd.read_csv("C:\\Users\\neha.yargal\\Documents\\LPS\\WorkDayData\\TAAData\\TAA_Holiday_Calendar.csv",parse_dates=['Date'],skiprows=1)
        TAA_Holiday_Calendar['Date'] = pd.to_datetime(TAA_Holiday_Calendar['Date'])
        TAAOrganizationTime = TAAOrganizationTime.fillna(value='None')
        TAATimeOff = TAATimeOff.fillna(value='None')
        TAA_Holiday_Calendar = TAA_Holiday_Calendar.fillna(value='None')

        pattern = r"^US\d\d-.*?\s"
        with connection.cursor() as cursor:
            for index, row in TAAOrganizationTime.iterrows():
                # Make sure the order of the values matches the order of the columns in the table
            
                try:
                    #  cursor.execute("exec temp_sp_updateProjectTable @projectNumber = ?, @objective = ?, @type = ?, @stage = ?, @customerID = ?, @siteID = ?,@divisionID = ?, @modifiedBy = ?",row['ProjectNumber'], row['Objective'], row['Type'], row['Stage'],  row['CustomerID'], row['SiteID'], row['DivisionID'], row['ModifiedBy'])
                    # if row['Project']=='NULL':
                    #     projectNumber = None
                    # else :
                    projectNumber = row['Project']
                    if re.match(pattern, projectNumber):                                           
                        projectNumber = re.split(r"\s", projectNumber, maxsplit=1)[0]
                    else:
                        projectNumber = row['Project'].split('_')[0]
                    query = 'exec AddTAAOrganizationTimeToWDAllHours %s, %s, %s, %s, %s, %s, %s, %s, %s'
                    args = (row['EE ID'], row['Worker'], projectNumber, row['Manager'], row['Project'], row['Status'], row['Date'],format(row['Hours'],'.2f'), row['Comment'])
                    cursor.execute(query, args)
                    # cursor.execute("exec AddTAAOrganizationTimeToWDAllHours @EEID = ?, @WorkerName = ?, @ProjectNumber = ?, @Manager = ?, @ProjectCode = ?, @Status = ?,@WDate = ?, @HoursWorked = ?, @Comment= ?",row['EE ID'], row['Worker'], projectNumber, row['Manager'], row['Project'], row['Status'], row['Date'],format(row['Hours'],'.2f'), row['Comment'])
                except Exception as err:
                        # logger.logger.error("Error :[%s] [%s] ",err, row['ProjectNumber'])
                        log.logger.error("TAAOrganizationTime Error :[%s] [%s] [%s]",err, row['Worker'],row['Date'])
            cursor.commit()

            log.logger.info('Import All Worker Time Off Table to DB.')
            #Import All Worker Time Off Table to DB
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            for index, row in TAATimeOff.iterrows():
                
                try:
                    if 'Approved' in TAATimeOff.columns and row['Approved'] != 'None':
                        status = 'Approved'   
                        hours = row['Approved']
                    elif 'Denied' in TAATimeOff.columns and row['Denied']  != 'None':
                        status = 'Denied' 
                        hours = row['Denied']
                    elif 'Pending' in TAATimeOff.columns and row['Pending'] !='None':
                        status = 'Pending' 
                        hours = row['Pending']
                    # print(row['Time Off Date'].to_pydatetime().strftime('%m/%d/%Y'))
                    # print(datetime.strptime(row['Entered On'].to_pydatetime().strftime('%m/%d/%Y'),'%m/%d/%Y').date())
                    query = 'exec AddTAAOrganizationTimeToWDAllHours %s, %s, %s, %s, %s, %s, %s, %s, %s'
                    args = (None, row['Worker'], 'PTO', row['Supervisory Organization'], 'PTO', status, row['Time Off Date'].to_pydatetime().strftime('%m/%d/%Y'), hours, None)
                    cursor.execute(query, args)
                    # cursor.execute("exec AddTAAOrganizationTimeToWDAllHours @WorkerName = ?, @ProjectNumber = ?, @Manager = ?, @ProjectCode = ?, @Status = ?,@WDate = ?, @HoursWorked = ?", row['Worker'], 'PTO', row['Supervisory Organization'], 'PTO', status, row['Time Off Date'].to_pydatetime().strftime('%m/%d/%Y'), hours)
                except Exception as err:
                        log.logger.error("TAATimeOFF Error :[%s] [%s] [%s]",err, row['Worker'],row['Time Off Date'])

            cursor.commit()

            log.logger.info('Import All Holiday Table to DB.')
            # Import All Holiday Table to DB
            #find the pay period
            startDate = TAAOrganizationTime['Date'][0] - to_offset("1D")
            endDate = TAAOrganizationTime['Date'][len(TAAOrganizationTime.index)-1]
            # startDate + to_offset("13D")
            #TAAOrganizationTime['Date'][len(TAAOrganizationTime.index)-1]
            print("StartDay:",startDate)
            print("EndDate:",endDate)
            #find the hohliday from holiday calender during that pay period
            TAA_Holiday_Calendar = TAA_Holiday_Calendar.query('Date >= @startDate and Date <= @endDate')

            workerList = pd.unique(TAAOrganizationTime[['Worker']].values.ravel())
            if len(TAA_Holiday_Calendar) != 0:
                for index, row in TAA_Holiday_Calendar.iterrows():
                    for worker in workerList:
                        try:
                            # print(TAAOrganizationTime.query(f'Worker == @worker')['Manager'].values[0])
                            query = 'exec AddTAAOrganizationTimeToWDAllHours %s, %s, %s, %s, %s, %s, %s, %s, %s'
                            args = (None, worker,'Holiday', TAAOrganizationTime.query(f'Worker == @worker')['Manager'].values[0],'Holiday','Approved', row['Date'].to_pydatetime().strftime('%m/%d/%Y'),8,None)
                            cursor.execute(query, args)
                            # cursor.execute("exec AddTAAOrganizationTimeToWDAllHours @WorkerName = ?, @ProjectNumber = ?, @Manager = ?, @ProjectCode = ?, @Status = ?,@WDate = ?, @HoursWorked = ?",worker,'Holiday', TAAOrganizationTime.query(f'Worker == @worker')['Manager'].values[0],'Holiday','Approved', row['Date'].to_pydatetime().strftime('%m/%d/%Y'),8)
                        except Exception as err:
                            log.logger.error("TAAHoliday Error :[%s] [%s] [%s]",err, row['Worker'],row['Date'])
                cursor.commit()
                
            log.logger.info('Success!')
            return Response('Workday OK')
    except Exception as err:
                    log.logger.error("Error :[%s]",err)
    # finally:
    #     # # Close the database connection
    #     return Response('Workday OK')