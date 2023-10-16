'''
Utility functions for output

Created on Jan 03, 2019

@author: ZE
'''

from datetime import datetime
import pandas as pd

def print_profile_result(result):
    ending = ', '
    print('Date', end = ending)
    for i in range(0, len(result.header)):
        if (i == len(result.header) - 1):
            ending = '\n'
        
        if (result.header[i].caption != None):
            print(result.header[i].option, end = ending)
        elif (result.header[i].formula != None):
            print(result.header[i].formula, end = ending)
        elif (result.header[i].observation != None):
            print('%s' % (result.header[i].observation), end = ending)
        else:
            print(result.header[i].attribute[0].caption, end = ending)

    for row in range(0, len(result.data)):
        ending = ', '
        print(result.data[row].formattedDateString, end = ending)
        for col in range(0, len(result.data[row].result)):
            if (col == len(result.data[row].result) - 1):
                ending = '\n'
            print(result.data[row].result[col], end = ending)

def profile_result_to_df(result, raw=False):
    columns = []
    columns.append('Date')
    isHour = False
    isHourMinute = False
    if result.data[0].hour is not None:
        isHour = True
        columns.append('Hour')
    if result.data[0].minute is not None:
        isHourMinute = True
        columns.append('Minute')
        
    for i in range(0, len(result.header)):
        if result.header[i].caption is not None:
            columns.append(result.header[i].caption)
        elif raw and result.header[i].observation is not None:
            columns.append(result.header[i].observation)
        elif result.header[i].series is not None:
            columns.append(result.header[i].series)
        elif result.header[i].observation is not None:
            columns.append(result.header[i].observation)
        elif (result.header[i].formula is not None):
            columns.append(result.header[i].formula)
        else:
            columns.append(result.header[i].attribute[0].caption)

    df = {}
    for c in columns:
        df[c] = []
        
    for row in range(0, len(result.data)):
        i = 0
        df[columns[i]].append(datetime.strptime(result.data[row].date, "%m/%d/%Y").date())
        if isHour:
            i += 1
            if result.data[row].hour is not None:
                df[columns[i]].append(int(result.data[row].hour))
            else:
                df[columns[i]].append(None)
        if isHourMinute:
            i += 1
            if result.data[row].minute is not None:
                df[columns[i]].append(int(result.data[row].minute))
            else:
                df[columns[i]].append(None)
                
        for col in range(0, len(result.data[row].result)):
            i += 1
            df[columns[i]].append(result.data[row].result[col])
            
    return pd.DataFrame.from_dict(df)
    
def print_curve_bean(result):
    for c in result:
        print('ID: %d' % c.id)
        print('Name: %s' % c.name)
        print('Group name: %s' % c.groupName)
        print('Data type: %s' % c.dataType)
        print()
    
def curve_bean_to_df(result):
    df = {}
    columns = ['user', 'group', 'name', 'id', 'class', 'profile_name', 'config_name', 'curve_type', 'granularity', 'data_type']
    for c in columns:
        df[c] = []
    
    names = {}
    
    for b in result:                
        for p in b.profiles:
            if len(p.observations) == 0:
                df[columns[0]].append(b.owner)
                df[columns[1]].append(b.groupName)
                df[columns[2]].append(b.name)
                df[columns[3]].append(b.id)
                df[columns[4]].append(b.dataType)
                df[columns[5]].append(p.profileName)
                df[columns[6]].append(p.configName)
                df[columns[7]].append('')
                df[columns[8]].append(b.granularity)
                df[columns[9]].append('')
            else:
                for o in p.observations:
                    df[columns[0]].append(b.owner)
                    df[columns[1]].append(b.groupName)
                    df[columns[2]].append(b.name)
                    df[columns[3]].append(b.id)
                    df[columns[4]].append(b.dataType)
                    df[columns[5]].append(p.profileName)
                    df[columns[6]].append(p.configName)
                    df[columns[7]].append(o.curveType)
                    df[columns[8]].append(o.granularity)
                    df[columns[9]].append(o.dataType)
        
        if len(b.properties) > 0:
            for pp in b.properties:
                if pp.label in names:
                    names[pp.label] += 1
                else:
                    names[pp.label] = 1
    
    result_len = len(result)
    valid_names = []
    for n in names:
        if names[n] == result_len:
            valid_names.append(n)
            df[n] = []
    
    # only include properties assigned to all available curves
    if len(valid_names) > 0:
        for b in result:
            for pp in b.properties:
                if pp.label in valid_names:
                    for p in b.profiles:
                        if len(p.observations) == 0:
                            df[pp.label].append(pp.value)
                        else:
                            for o in p.observations:
                                df[pp.label].append(pp.value)
        
    return pd.DataFrame.from_dict(df)
    
def print_curve_data_bean(result):
    for r in result:
        print('Curve name: %s' % r.curveName)
        print('Opr date: %s' % r.oprDate)
        print('Curve type: %s' % r.curveType)
        print('Contract year: %d' % r.contractYear)
        print('Contract month: %d' % r.contractMonth)
        print('Value: %s' % r.value)
        print()

def print_forward_curve_data(result):
    for gd in result.groupedData:
        print('Key: %s' % gd.key)
        for fd in gd.data:
            print('\tCurve name: %s' % fd.curveName)
            print('\tOpr date: %s' % fd.oprDate)
            print('\tCurve type: %s' % fd.curveType)
            print('\tContract year: %d' % fd.contractYear)
            print('\tContract month: %d' % fd.contractMonth)
            print('\tValue: %s' % fd.value)
            print()

def forward_curve_to_df(result):
    df = {}
    columns = ['name', 'opr_date', 'contract_start', 'contract_end', 'contract_code', 'contract_year', 'type', 'value', 'date_modified']
    for c in columns:
        df[c] = []

    for gd in result.groupedData:
        for e in gd.data:
            df[columns[0]].append(e.curveName)
            df[columns[1]].append(e.oprDate.date())
            df[columns[2]].append(e.contractStart.date())
            df[columns[3]].append(e.contractEnd.date())
            df[columns[4]].append(e.contractMonth)
            df[columns[5]].append(e.contractYear)
            df[columns[6]].append(e.curveType)
            df[columns[7]].append(e.value)
            df[columns[8]].append(e.lastUpdated)
            
    return pd.DataFrame.from_dict(df)

def time_series_curve_to_df(result):
    df = {}
    columns = ['name', 'opr_date', 'opr_hour', 'opr_minute', 'type', 'value', 'date_modified']
    for c in columns:
        df[c] = []

    for gd in result.groupedData:
        for e in gd.data:
            df[columns[0]].append(e.curveName)
            df[columns[1]].append(e.oprDate.date())
            df[columns[2]].append(e.oprHour)
            df[columns[3]].append(e.oprMinute)
            df[columns[4]].append(e.curveType)
            df[columns[5]].append(e.value)
            df[columns[6]].append(e.lastUpdated)
            
    return pd.DataFrame.from_dict(df)

def options_curve_to_df(result):
    df = {}
    columns = ['name', 'opr_date', 'contract_start', 'contract_end', 'contract_code', 'contract_year', 'type',
               'put_call', 'level_type', 'level_value', 'strip_unit', 'spread_length', 'contract_start_2',
               'contract_end_2', 'contract_month_2', 'contract_year_2', 'value', 'date_modified']
    for c in columns:
        df[c] = []

    for gd in result.groupedData:
        for e in gd.curveData:
            df[columns[0]].append(e.curveName)
            df[columns[1]].append(e.oprDate.date())
            df[columns[2]].append(e.contractStart.date())
            df[columns[3]].append(e.contractEnd.date())
            df[columns[4]].append(e.contractMonth)
            df[columns[5]].append(e.contractYear)
            df[columns[6]].append(e.curveTypeName)
            df[columns[7]].append(e.putCall)
            df[columns[8]].append(e.levelType)
            df[columns[9]].append(e.levelValue)
            df[columns[10]].append(e.stripUnit)
            df[columns[11]].append(e.spreadLength)
            df[columns[12]].append(e.contractStart2.date())
            df[columns[13]].append(e.contractEnd2.date())
            df[columns[14]].append(e.contractMonth2)
            df[columns[15]].append(e.contractYear2)
            df[columns[16]].append(e.value)
            df[columns[17]].append(e.lastUpdated)
            
    return pd.DataFrame.from_dict(df)

def insert_update_curve_data_result_to_df(result):
    df = {}
    columns = ['curve_name', 'curve_id', 'opr_date', 'records_inserted', 'records_updated', 'records_deleted', 'valid']
    for c in columns:
        df[c] = [] 
        
    for e in result:
        df[columns[0]].append(e.curveName)
        df[columns[1]].append(e.curveId)
        df[columns[2]].append(e.oprDate)
        df[columns[3]].append(e.numRecordsInserted)
        df[columns[4]].append(e.numRecordsUpdated)
        df[columns[5]].append(e.numRecordsDeleted)
        df[columns[6]].append(e.valid)
    
    return pd.DataFrame.from_dict(df)
        
def print_time_series_curve_data(result):
    for gd in result.groupedData:
        print('Key: %s' % gd.key)
        for fd in gd.data:
            print('\tCurve name: %s' % fd.curveName)
            print('\tOpr date: %s' % fd.oprDate)
            if (fd.oprHour != None):
                print('\tOpr hour: %s' % fd.oprHour)
            print('\tCurve type: %s' % fd.curveType)
            print('\tValue: %s' % fd.value)
            print()

def print_options_curve_data(result):
    for gd in result.groupedData:
        print('Key: %s' % gd.key)
        for fd in gd.curveData:
            print('\tCurve name: %s' % fd.curveName)
            print('\tOpr date: %s' % fd.oprDate)
            print('\tCurve type: %s' % fd.curveTypeName)
            print('\tContract year: %d' % fd.contractYear)
            print('\tContract month: %d' % fd.contractMonth)
            print('\tPut / Call: %s' % fd.putCall)
            print('\tLevel type: %s' % fd.levelType)
            print('\tLevel value: %s' % fd.levelValue)
            print('\tStrip unit: %s' % fd.stripUnit)
            print('\tSpread length: %d' % fd.spreadLength)
            print('\tContract year 2: %d' % fd.contractYear2)
            print('\tContract month 2: %d' % fd.contractMonth2)
            print('\tValue: %s' % fd.value)
            print()
