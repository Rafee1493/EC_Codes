# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:51:38 2023

@author: AbdullahArRafee
"""

import pandas as pd
import numpy as np

x = pd.read_excel('FormattedAnalysisFile_2024_NYSLRS_Payrolls_8.12.24.xlsx',
                  sheet_name = 'Sheet1')

data = x.copy()

# Removing Special Districts for the tables

data =data[data['BranchName'] != "Special Districts"]

data["AgencyName"] = data["AgencyName"].str.strip()

#%% Adding Counties & Regions

match = pd.read_excel('C:/Users/AbdullahArRafee/OneDrive - Empire Configuration/SeeThroughNY/Reference/Match Files/Official Match Files/Region Match Document (Counties, Cities, Towns, Villages).xlsx',
                      sheet_name = 'Location Code Match', dtype = {'LOCATION_CODE': str})

data = data.merge(match, how = 'left', left_on = 'LOCATION_CODE', right_on = 'Location Code')


data = data.drop(columns = ['Location Code', 'Branch Name', 'Employer Name'])

#%% Creating the Tables for Website

## Top 10 Paid Employees - by Region

a = data.sort_values('YTDPay',ascending = False).groupby('Region').head(10)

a_1 = a[["Region","WholeName","AgencyName", "BranchName", "RET_SYSTEM", "YTDPay"]]

col_name = {"Region" : "Region",
            "WholeName" : "Name",
            "AgencyName" : "Municipality",
            "BranchName" : "Municipality Type",
            "RET_SYSTEM" : "Employee Type", 
            "YTDPay" : "Total Pay"}

a_2 = a_1.rename(columns = col_name)

replace_val = {'PFRS' : 'Police/Fire',
           'ERS' : 'General Employee'}

a_2['Employee Type'] = a_2['Employee Type'].replace(replace_val)

a_2["Municipality"] = a_2["Municipality"].str.title()
a_2['Rank'] = a_2.groupby('Region')['Total Pay'].rank(method='first', ascending=False).astype(int)


#%% Top 50 Paid Employees - statewide


b = data.sort_values('YTDPay',ascending = False).head(50)

b_1 = b[["WholeName","AgencyName", "BranchName", "RET_SYSTEM", "YTDPay"]]

b_2 = b_1.rename(columns = col_name)
b_2['Employee Type'] = b_2['Employee Type'].replace(replace_val)

b_2["Municipality"] = b_2["Municipality"].str.title()
b_2['Rank'] = b_2['Total Pay'].rank(method='first', ascending=False).astype(int)


#%% Average Pay By Employee Type By Municipality

c = data[["Region", "BranchName", "AgencyName", "RET_SYSTEM", "YTDPay"]]

c_1 = c.rename(columns = col_name)

c_1['Employee Type'] = c_1['Employee Type'].replace(replace_val)
c_1["Municipality"] = c_1["Municipality"].str.title()

c_2 = c_1.groupby(["Region", "Municipality Type", "Municipality", "Employee Type"])["Total Pay"].agg(["count","mean"])

c_3 = c_2.rename(columns = {"mean" : "Average Pay",
                            "count" : "Employee Count"})

c_3.reset_index(inplace=True)



#%% Average Pay By Region

d = data[["Region", "RET_SYSTEM", "YTDPay"]]

d['RET_SYSTEM'] = d['RET_SYSTEM'].replace(replace_val)

d_1 = d.groupby(["Region", "RET_SYSTEM"])["YTDPay"].mean()

d_2 = d_1.unstack('Region')


#%% Saving

# CSV Files
a_2.to_csv("Top10EmployeesByRegion.csv", index = False)
b_2.to_csv("Top50EmployeesStatewide.csv", index = False)
c_3.to_csv("AveragePayByEmployeeTypeMuni.csv", index = False)
d_2.to_csv("AveragePayByRegion.csv", index = False)

# One Excel

name = 'AnalysisTables_2024_NYSLRS_Payrolls.xlsx'

with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
    # Save the DataFrames to separate sheets
    a_2.to_excel(writer, sheet_name='Top10byRegion', index=False)
    b_2.to_excel(writer, sheet_name='Top50', index=False)
    c_3.to_excel(writer, sheet_name='AvgbyMuni&EmpType', index=False)
    d_2.to_excel(writer, sheet_name='AvgbyRegion', index=False)
    
#%%

data['BranchName'].value_counts()
c_1.to_excel("x.xlsx", index = False)
