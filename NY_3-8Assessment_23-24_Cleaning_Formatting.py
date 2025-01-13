# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 18:16:17 2023

@author: abdul
"""

#%%

# Notes:
    # Change "db_file_path" to the filepath of the access database for the current year.
    # Change Year data while filtering, based on the year on which you are working on. 
    # Also change the school year later, when adding a new column
    # Change & Update the School Districts & Entity Names Match File Paths
    

#%% Connecting to access database - The output is two dataframes; one fro ela and other for math

import pyodbc
import pandas as pd
import numpy as np

# Database file path
db_file_path = r'C:/Users/abdul/OneDrive - Empire Configuration/SeeThroughNY/Education/NYSED Datasets/2023-24/Report Card Database/SRC2024_Group1/SRC2024_Group1.accdb'

# Connection string (assuming you have an ODBC driver set up for Access)
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    rf'DBQ={db_file_path};'
)

try:
    # Connect to the database
    conn = pyodbc.connect(conn_str)

    # Create a cursor
    cursor = conn.cursor()

    # Define the names of the tables you want to convert
    table1_name = "Annual EM ELA"  # Replace with your table name
    table2_name = "Annual EM MATH" ## Replace with your table name
    
    # Initialize empty lists to store rows and column names for each table
    rows_table1 = []
    rows_table2 = []
    column_names_table1 = []
    column_names_table2 = []
    
    # Fetch data from the first table (ela)
    query_table1 = f"SELECT * FROM [{table1_name}]"
    cursor.execute(query_table1)
    column_names_table1 = [column[0] for column in cursor.description]
    rows_table1 = [list(row) for row in cursor.fetchall()]
    
    # Fetch data from the second table (math)
    query_table2 = f"SELECT * FROM [{table2_name}]"
    cursor.execute(query_table2)
    column_names_table2 = [column[0] for column in cursor.description]
    rows_table2 = [list(row) for row in cursor.fetchall()]


    # Create DataFrames for each table
    ela = pd.DataFrame(rows_table1, columns=column_names_table1)
    math = pd.DataFrame(rows_table2, columns=column_names_table2)


except pyodbc.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and the connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()

#%% Combining the two subjects

ela_data = ela.copy()
math_data = math.copy()

ela_data['Subject Area'] = 'ELA'
math_data['Subject Area'] = 'Math'

data = pd.concat([ela_data,math_data])


#%% Initial Filtering

keep1 = ['ENTITY_CD', 'ENTITY_NAME', 'Subject Area', 'ASSESSMENT_NAME','SUBGROUP_NAME', 'TOTAL_COUNT', 'NUM_TESTED', 'NUM_PROF', 'YEAR']

data = data[keep1]

rep = ['TOTAL_COUNT','NUM_TESTED', 'NUM_PROF']

for i in rep:
    data[i] = data[i].replace('s', 0)
    
datatype = {'ENTITY_CD' : str,
            'ENTITY_NAME' : str,
            'Subject Area' : str,
            'ASSESSMENT_NAME' : str,
            'SUBGROUP_NAME' : str,
            'TOTAL_COUNT' : float,
            'NUM_TESTED' : float,
            'NUM_PROF' : float,
            'YEAR' : float}

data = data.astype(datatype)  

# Filtering for the subgroups we need

subgroup_filter = ['All Students', 'Female', 'Male', 'General Education Students', 'Students with Disabilities', 
                   'Asian or Native Hawaiian/Other Pacific Islander', 'Black or African American', 'Hispanic or Latino', 'White',
                   'Multiracial', 'Economically Disadvantaged', 'Not Economically Disadvantaged', 'English Language Learner',
                   'Non-English Language Learner', 'Not Migrant', 'American Indian or Alaska Native', 'Migrant']

data1 = data[data['SUBGROUP_NAME'].isin(subgroup_filter)]

# Filtering for the year

data1 = data1[data1['YEAR'] == 2024]

# Selecting only Grade 3 to 8 level data.

assessment_filter = ['ELA3','ELA4','ELA5','ELA6','ELA7','ELA8','MATH3','MATH4','MATH5','MATH6','MATH7','MATH8']  

data2 = data1[data1['ASSESSMENT_NAME'].isin(assessment_filter)]


# Removing Special Districts and counties

drop = ["000000000000","000000000001","000000000002","000000000003","000000000004","000000000005","000000000006","000000000007","000000000008","000000000009","111111111111"]

for i in drop:
    data2 = data2[data2["ENTITY_CD"] != i]

# Removing Counties

data2["BEDS_left"] = data2["ENTITY_CD"].str[:4]
data2 = data2[data2["BEDS_left"] != "0000"]




#%% Aggregation & Subsequent Calculations

data_grouped = data2.groupby(by = ['ENTITY_CD', 'ENTITY_NAME', 'Subject Area','SUBGROUP_NAME']).agg({"TOTAL_COUNT" : "sum",
                                                                                                  "NUM_TESTED": "sum",
                                                                                                  "NUM_PROF" : "sum"})

data_grouped.reset_index(inplace=True)

data_grouped['% Tested'] = round(((data_grouped['NUM_TESTED']/data_grouped['TOTAL_COUNT'])*100),0)
data_grouped['Proficiency Rate(%)'] = round(((data_grouped['NUM_PROF']/data_grouped['NUM_TESTED'])*100),0)

data_grouped['% Tested'] = data_grouped['% Tested'].replace([np.inf, -np.inf], 0)
data_grouped['% Tested'] = data_grouped['% Tested'].replace(np.nan, 0)
data_grouped['Proficiency Rate(%)'] = data_grouped['Proficiency Rate(%)'].replace([np.inf, -np.inf], 0)
data_grouped['Proficiency Rate(%)'] = data_grouped['Proficiency Rate(%)'].replace(np.nan, 0)         


#%% Assigning School Districts

sd = pd.read_excel('C:/Users/abdul/OneDrive - Empire Configuration/SeeThroughNY/Education/SchoolDistrictCodes_MatchFile.xlsx', sheet_name='SD Codes', dtype=str)

data_grouped['SD']  = data_grouped['ENTITY_CD'].str[0:6]

data_sd = data_grouped.merge(sd, left_on = 'SD', right_on = 'District Code', how = 'left')

#%% Assigning Entity Types

data_sd['Last 4'] = data_sd['ENTITY_CD'].str[-4:]
data_sd['7n8'] = data_sd['ENTITY_CD'].str[6:8]

data_sd["Entity Type"] = np.where(data_sd["Last 4"] == "0000", "District Overall", 
                                  np.where(data_sd["7n8"] == "86", "Charter", "District School"))

data_sd['Grade'] = 'Grade 3-8'
data_sd['School Year'] = '2023-24' 

#%% Fixing School Names

ec = pd.read_excel('C:/Users/abdul/OneDrive - Empire Configuration/SeeThroughNY/Education/SchoolDistrictCodes_MatchFile.xlsx', sheet_name='Entity Codes', dtype=str)

data_ec = data_sd.merge(ec, left_on = 'ENTITY_CD', right_on = 'BEDSCODE', how = 'left')

# At this point check if there are any new schools that are unrecorded in the matchfile. If yes, check and update the matchfile, and then rerun this section of code again.

#%% Retaining required columns

keep2 = ['ENTITY_CD', 'Entity Name (Proper)', 'School District Name_x', 'Entity Type', 'Subject Area', 'Grade', 'SUBGROUP_NAME', 
         'TOTAL_COUNT', 'NUM_TESTED', 'NUM_PROF', '% Tested', 'Proficiency Rate(%)', 'County', 'Region', 'School Year']
        

fin_data = data_ec[keep2]

col_rename = {    'ENTITY_CD' :  "BEDSCODE",
                  'Entity Name (Proper)' : "Entity Name",
                  'School District Name_x' : "School District Name",
                  'Entity Type' : "Entity Type",
                  'Subject Area' : "Subject Area",
                  'Grade' : "Grade",
                  'SUBGROUP_NAME' : "Sub Group",
                  'TOTAL_COUNT' : "Total Students",
                  'NUM_TESTED' : "Total Tested",
                  'NUM_PROF' : "Proficiency Count",
                  '% Tested' : "% Tested",
                  'Proficiency Rate(%)' : "Proficiency Rate(%)",
                  'County' : "County",
                  'Region' : "Region",
                  'School Year' : "School Year"}

fin_data = fin_data.rename(columns=col_rename)

#%% Saving

fin_data.to_excel('FormattedFile_NYS_3-8_Assessment_2023-24.xlsx', index = False)

#%%

data2['SUBGROUP_NAME'].value_counts()
data_ec.to_excel('test.xlsx', index = False)














