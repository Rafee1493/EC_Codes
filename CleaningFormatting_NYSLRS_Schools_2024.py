# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:58:35 2023

@author: AbdullahArRafee
"""

import pandas as pd
import numpy as np

data2024 = pd.read_csv('FormattedFile_2024_NYSLRS_Payrolls_Schools_8.12.24.csv')


#%% Cleaning 2024 Data

data2024["SubAgencyName"] = "NYSLRS - General Employee"

col_rename = {'DATE_OF_MEMBERSHIP' : 'Date of Membership',
              'WholeName' : 'WholeName',
              'EARNINGS' : 'YTDPay',
              'SubAgencyName' : 'SubAgencyName', 
              'EMPLOYER_NAME' : 'AgencyName',
              'PayYear' : 'PayYear',
              'BranchName_x': 'BranchName',
              'JOB_CODE_DESCRIPTION': 'PositionName',
              'PayBasis': 'PayBasis',
              'Rate': 'Rate',
              'LOCATION_CODE' : 'LOC_CODE',
              'JOB_CODE' : 'JOBCODE'}

data2024 = data2024.rename(columns=col_rename)

# Updating Employer Names (Agency Names) from Match document

match = pd.read_excel("C:/Users/abdul/OneDrive - Empire Configuration/SeeThroughNY/Reference/Match Files/Official Match Files/Schools_Master_Match_File_9.24.24.xlsx", sheet_name = 'NYSLRS Match')

data2024_n = data2024.merge(match, how = 'left', left_on = 'AgencyName' , right_on = 'OriginalName')

data2024_n = data2024_n.drop(['AgencyName_x', 'OriginalName', 'AgencyName (Old)'], axis = 1)

data2024_n = data2024_n.rename(columns = {'AgencyName_y' : 'AgencyName'})


# Reorder Columns

data2024_n = data2024_n[['BranchName', 'AgencyName', 'SubAgencyName', 'WholeName', 'PositionName', 'PayBasis', 'Rate', 'YTDPay', 'PayYear', 'Date of Membership', 'RET_SYSTEM', 'LOC_CODE', 'JOBCODE', 'County', 'Region']]



#%% Saving

data2024_n.to_excel('FormattedFile_2024_NYSLRS_Schools_(For NYSTRS)_9.25.24.xlsx', index = False)



#%%

data2024_n.columns

data2024_n.to_csv('x.csv', index = False)

