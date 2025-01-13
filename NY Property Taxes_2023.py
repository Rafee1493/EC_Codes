# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:43:28 2024

@author: AbdullahArRafee
"""

import pandas as pd
import numpy as np

counties = pd.read_excel("Countiesleveltwo23.xlsx")
cities = pd.read_excel("Citiesleveltwo23.xlsx")
towns = pd.read_excel("Townsleveltwo23.xlsx")
villages = pd.read_excel("Villagesleveltwo23.xlsx")
sd = pd.read_excel("Schoolsleveltwo23.xlsx")

#%% Cleanup - 1: For all tables

# Applying common cleaning operations to all the dataframes by defining a 'cleaning' function

def cleaning(df):
    df = df[:-3]                                            #Removing last 3 rows  
    df = df[4:].reset_index(drop=True)                      #Removing first 4 rows                                       
    df.columns = df.iloc[0]                                 #takes the first row and sets it as the column headers.
    df = df.drop(0).reset_index(drop=True)                  #drops the first row, as it's now the header.
    df.columns = df.columns.str.replace('\n', '', regex=False)
    df['Real Property Taxes'] = df['Real Property Taxes'].replace('Not Filed', np.nan)
    return df

df = [counties, cities, towns, villages, sd]

processed_dataframes = [cleaning(i) for i in df]

counties_p = processed_dataframes[0]
cities_p = processed_dataframes[1]
towns_p = processed_dataframes[2]
villages_p = processed_dataframes[3]
sd_p = processed_dataframes[4]

#%% Clean up - Counties

match = pd.read_excel('C:/Users/AbdullahArRafee/OneDrive - Empire Configuration/SeeThroughNY/Reference/Match Files/Official Match Files/Region Match Document (Counties, Cities, Towns, Villages).xlsx',sheet_name = "Counties")

co_p_1 = counties_p.merge(match, how = 'left', left_on = "County", right_on = "County")


# Fixing relevant nan column names

for index, column_name in enumerate(co_p_1.columns):                                        # Use this to find the index for next code
    print(f"Index: {index}, {column_name}")

co_p_1.columns = co_p_1.columns.fillna('Unknown')                                           # Changing all NaN column names to 'Unknown'
co_p_1.columns.values[178] = 'Total Expenditures'                                           # Check the above code to locate the nan column and its index. Be careful


# Converting data to numeric

dtypes = {'2020 Population' : float,
          'Land Area (Sq. Mi.)' : float,
          'Full Value' : float,
          'Debt Outstanding' : float,
          'Real Property Taxes' : float,
          'Miscellaneous Non-Property Taxes' : float,
          'Special Assessments' : float,
          'Star Payments' : float,
          'Payments in Lieu of Taxes' : float,
          'Gain from Sale of Tax Acquired Property' : float,
          'Interest & Penalties' : float,
          'Miscellaneous Tax Items' : float,
          'Sales Tax' : float,
          'Sales Tax Distribution' : float,
          'Utilities Gross Receipts Tax' : float,
          'Miscellaneous Use Taxes' : float,
          'Franchises' : float,
          'Emergency Telephone System Surcharge' : float,
          'City Income Tax' : float,
          'Miscellaneous Non-Property Taxes' : float,
          'Total Expenditures' : float}

co_p_1 = co_p_1.astype(dtypes,errors = 'ignore')

## Columns & Calculations

# Size column

co_p_1['Size'] = pd.np.where(co_p_1['2020 Population']<=100000, 'Small',
                             pd.np.where(co_p_1['2020 Population']<=900000, 'Medium', 'Large'))

# Other Calc

co_p_1['Full Value Per Capita'] = co_p_1['Full Value']/co_p_1['2020 Population']
co_p_1['Tax Per Capita'] =(co_p_1[['Real Property Taxes',
                                   'Special Assessments',
                                   'Star Payments',
                                   'Payments in Lieu of Taxes',
                                   'Gain from Sale of Tax Acquired Property',
                                   'Interest & Penalties',
                                   'Miscellaneous Tax Items',
                                   'Sales Tax',
                                   'Sales Tax Distribution',
                                   'Utilities Gross Receipts Tax',
                                   'Miscellaneous Use Taxes',
                                   'Franchises',
                                   'Emergency Telephone System Surcharge',
                                   'City Income Tax',
                                   'Miscellaneous Non-Property Taxes']].sum(axis=1))/co_p_1['2020 Population']
co_p_1['Debt Per Capita'] = co_p_1['Debt Outstanding']/co_p_1['2020 Population']
co_p_1['Expenditure Per Capita'] = co_p_1['Total Expenditures']/co_p_1['2020 Population']
co_p_1['Real Property Taxes Per Capita'] = co_p_1['Real Property Taxes']/co_p_1['2020 Population']
co_p_1['Effective Property Tax Rate'] = co_p_1['Real Property Taxes Per Capita']/co_p_1['Full Value Per Capita']
co_p_1['Special Assessments Per Capita'] = co_p_1['Special Assessments']/co_p_1['2020 Population']
co_p_1['Real Property Taxes and Assessments Per Capita'] = co_p_1['Real Property Taxes Per Capita'] + co_p_1['Special Assessments Per Capita']

# Final County table

county_final = co_p_1[['Muni Code', 'Region', 'Major Area', 'County', 'Size', '2020 Population', 'Land Area (Sq. Mi.)', 
                       'Full Value Per Capita', 'Effective Property Tax Rate', 'Tax Per Capita', 'Debt Per Capita', 'Expenditure Per Capita']]

#%% Clean up - Cities

cities_p['City'] = cities_p['Entity Name'].str[8:]

match = pd.read_excel('C:/Users/AbdullahArRafee/OneDrive - Empire Configuration/SeeThroughNY/Reference/Match Files/Official Match Files/Region Match Document (Counties, Cities, Towns, Villages).xlsx',sheet_name = "Cities")

cities_p_1 = cities_p.merge(match, how = 'left', left_on = "City", right_on = "City.1")

# Fixing relevant nan column names

for index, column_name in enumerate(cities_p_1.columns):                                        # Use this to find the index for next code
    print(f"Index: {index}, {column_name}")

cities_p_1.columns = cities_p_1.columns.fillna('Unknown')                                       # Changing all NaN column names to 'Unknown'
cities_p_1.columns.values[178] = 'Total Expenditures'                                           # Check the above code to locate the nan column and its index. Be careful


# Converting data to numeric

dtypes = {'2020 Population' : float,
          'Land Area (Sq. Mi.)' : float,
          'Full Value' : float,
          'Debt Outstanding' : float,
          'Real Property Taxes' : float,
          'Miscellaneous Non-Property Taxes' : float,
          'Special Assessments' : float,
          'Star Payments' : float,
          'Payments in Lieu of Taxes' : float,
          'Gain from Sale of Tax Acquired Property' : float,
          'Interest & Penalties' : float,
          'Miscellaneous Tax Items' : float,
          'Sales Tax' : float,
          'Sales Tax Distribution' : float,
          'Utilities Gross Receipts Tax' : float,
          'Miscellaneous Use Taxes' : float,
          'Franchises' : float,
          'Emergency Telephone System Surcharge' : float,
          'City Income Tax' : float,
          'Miscellaneous Non-Property Taxes' : float,
          'Total Expenditures' : float}

cities_p_1 = cities_p_1.astype(dtypes,errors = 'ignore')

## Columns & Calculations

# Size column

cities_p_1['Size'] = pd.np.where(cities_p_1['2020 Population']<=10000, 'Small',
                             pd.np.where(cities_p_1['2020 Population']<=90000, 'Medium', 'Large'))

# Other Calc

cities_p_1['Full Value Per Capita'] = cities_p_1['Full Value']/cities_p_1['2020 Population']
cities_p_1['Tax Per Capita'] =(cities_p_1[['Real Property Taxes',
                                   'Special Assessments',
                                   'Star Payments',
                                   'Payments in Lieu of Taxes',
                                   'Gain from Sale of Tax Acquired Property',
                                   'Interest & Penalties',
                                   'Miscellaneous Tax Items',
                                   'Sales Tax',
                                   'Sales Tax Distribution',
                                   'Utilities Gross Receipts Tax',
                                   'Miscellaneous Use Taxes',
                                   'Franchises',
                                   'Emergency Telephone System Surcharge',
                                   'City Income Tax',
                                   'Miscellaneous Non-Property Taxes']].sum(axis=1))/cities_p_1['2020 Population']
cities_p_1['Debt Per Capita'] = cities_p_1['Debt Outstanding']/cities_p_1['2020 Population']
cities_p_1['Expenditure Per Capita'] = cities_p_1['Total Expenditures']/cities_p_1['2020 Population']
cities_p_1['Real Property Taxes Per Capita'] = cities_p_1['Real Property Taxes']/cities_p_1['2020 Population']
cities_p_1['Effective Property Tax Rate'] = cities_p_1['Real Property Taxes Per Capita']/cities_p_1['Full Value Per Capita']
cities_p_1['Special Assessments Per Capita'] = cities_p_1['Special Assessments']/cities_p_1['2020 Population']
cities_p_1['Real Property Taxes and Assessments Per Capita'] = cities_p_1['Real Property Taxes Per Capita'] + cities_p_1['Special Assessments Per Capita']

cities_p_1 = cities_p_1.rename(columns = {'County_x' : 'County',
                                          'City_x' : 'City'})

# Final County table

city_final = cities_p_1[['Muni Code', 'City', 'Region', 'Major Area', 'County', 'Size', '2020 Population', 'Land Area (Sq. Mi.)', 
                       'Full Value Per Capita', 'Effective Property Tax Rate', 'Tax Per Capita', 'Debt Per Capita', 'Expenditure Per Capita']]


#%%

# !Replace NaNs with "Not Filed'!

co_p_1.to_excel('x.xlsx', index = False)

co_p_1.columns
