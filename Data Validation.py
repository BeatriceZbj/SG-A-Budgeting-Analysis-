from interval import Interval
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import re





def check_Basic(datatable):
    # Check the shape of dataset
    print(datatable.shape)
    # Check the basic info of dataset
    print(datatable.info())
    # Check the Null
    print(datatable.isnull())
    # Check Columns
    print(datatable.columns)
    # Check the head of the data
    print(datatable.head(20))
    # Check the tail of the data
    print(datatable.tail(20))



def check_date(datatable):
    # The Hire Date should be prior to the Status Date
    global HireDate 
    HireDate = pd.to_datetime(datatable['db_hire_dt'])
    StatusDate = pd.to_datetime(datatable['db_stat_dt'])
    timediff = StatusDate - HireDate
    i = 0
    for time in timediff:
        if time.days < 0:
            i += 1
            print(i)

def check_Unique(datatable):
    # The ID should be unique to reprensent different Employees
    UniqueNumber_of_Empid = len(datatable.empid.unique())
    UniqueNumber_of_Empid_mgr = len(datatable.empid_mgr.unique())
    UniqueNumber_of_userdid = len(datatable.db_userdid.unique())
    print('Number of Unique Employees ID' + ' : ' + str(UniqueNumber_of_Empid) +'\n'+
    'Number of Unique Mgr ID' + ' : ' + str(UniqueNumber_of_Empid_mgr) + '\n' + 
    'Number of Unique Userid' + ' : ' + str(UniqueNumber_of_userdid))

def check_Consistency(datatable):
    # If the value of the PriorCenter is null, the Prior Center Date should be null
    PriorCenter = datatable.db_prior_center.isnull()
    PriorCenterDate = datatable.db_prior_center_dt.isnull()
    for i,j in zip(PriorCenter,PriorCenterDate):
        if i != j:
            print('fail')


def check_Outlier(datatablemerge):
    Group_Mean_Std = datatablemerge.Amount.groupby(datatablemerge.db_functional_title1).agg(['mean','std'])
    Titletype = datatablemerge.db_functional_title1.unique()

    for title in Titletype:
        Outlier = []
        i = 0
        while i < 5:
            TypeAmount = datatablemerge[datatablemerge.db_functional_title1 == title].Amount
            Z_Score = abs((TypeAmount - Group_Mean_Std.iloc[i,0]))/Group_Mean_Std.iloc[i,1]
            i += 1
            for score in Z_Score:
                if score >= 3.5:
                    Outlier.append(score)
        print(title + ':' + str(len(Outlier)))
                    

def check_digit(datatable):
    Sixdigit = []
    LessSixdigit = []
    OverSixdigit = []
    for i in datatable.empid:
        if len(str(i)) == 6:
            Sixdigit.append(i)
        elif len(str(i)) < 6 :
            LessSixdigit.append(i)
        else:
            OverSixdigit.append(i)
    print(len(Sixdigit))
    print(len(LessSixdigit))
    print(len(OverSixdigit))


def check_Completeness(datatable):
    x = range(len(datatable))
    y = datatable.empid
    plt.scatter(x, y)
    plt.xlabel('Number of Records')
    plt.ylabel('Employees ID')
    plt.show()

def check_Syntax(datatable):
    userid = datatable.db_userdid
    mgruserid = datatable.db_managed_userid
    for i,j in zip(userid,mgruserid):
        if re.match(r'^[A-Z]\d{5}$', i) == None and re.match(r'^[A-Z]\d{5}$', j) == None:
            print('error!')

def check_datebound(datatable):
    HireDate = pd.to_datetime(datatable['db_hire_dt'])
    StatusDate = pd.to_datetime(datatable['db_stat_dt'])
    start = '2019-01-01'
    end = '2019-12-31'
    datestart = dt.datetime.strptime(start, r'%Y-%m-%d')
    dateend = dt.datetime.strptime(end, r'%Y-%m-%d')
    datebound = Interval(datestart, dateend)
    for i,j in zip(HireDate, StatusDate):
        if i not in datebound or j not in datebound:
            print('error!')

def main():
    datatableSource = pd.read_excel('Project Part 2 HR Data.xlsx',sheet_name = [0,1])
    datatable = datatableSource[0]
    datatable1 = datatableSource[1]
    datatablemerge = pd.merge(datatable, datatable1, on = 'db_userdid', how = 'inner')
    # check_Basic(datatable)
    # check_date(datatable)
    # check_Unique(datatable)
    # check_Consistency(datatable)
    # check_Outlier(datatablemerge)
    # check_digit(datatable)
    # check_Completeness(datatable)
 
    
            

main()