# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:21:12 2023

@author: AbdullahArRafee
"""

#%%

import pandas as pd
import numpy as np

x = pd.read_excel('OriginalData.NYSLRS.Actives.FY2024.7.26.24.xlsx', dtype = {'LOCATION_CODE': str,
                                                                              'JOB_CODE': str})

data = x.copy()

#%% Initial Cleaning & Others

data = data.rename(columns = {'LAST_NAME' : 'Last Name',
                              'FIRST_NAME' : 'First Name',
                              'MIDDLE_NAME/INITIAL' : 'MI'})
                   
data["Last Name"] = data["Last Name"].str.replace(" I V"," IV")

col = ['Last Name', 'First Name', 'MI']

for i in col:
    data[i] = data[i].str.upper()                                           # Coverting all to upper
    data[i] = data[i].str.strip()                                           # Removing leading & trailing white spaces in the names
    data[i] = data[i].replace("\d+", "", regex=True)                        # Removing numbers
    data[i] = data[i].replace(r"[^\w\s']", "", regex=True)                  # Removing  special characters except Apostrophe (')
    data[i] = data[i].str.replace(",","")                                   # Replacing commas
    

# Removing double spacing - Run this multiple times to remove all more than double spaces                            
for _ in range(3):
    data["First Name"] = data["First Name"].str.replace("  "," ")
    data["Last Name"] = data["Last Name"].str.replace("  "," ")                 
    data["MI"] = data["MI"].str.replace("  "," ")


#%% Fixing Names - Separating Suffixes - Last Name

## This dataset has suffixes in First Name, Last Name, and MI. First Name upto III (and jr), Last Name upto IV, MI upto III (and Jr).

# First we identify suffixes in Last Names
# For this dataset there are suffixes upto IV.

# First we check the number of columns it will split into. 
y = data["Last Name"].str.split(" ", expand=True)

data[["L1","L2","L3","L4","L5"]] = data["Last Name"].str.split(" ", expand=True)

full_l = ["L1","L2","L3","L4","L5"]
one_l = ["L2","L3", "L4","L5"]
two_l = ["L1","L3","L4","L5"]
three_l = ["L1","L2","L4","L5"]
four_l = ["L1","L2","L3","L5"]
five_l = ["L1","L2","L3","L4"]

#%% Fixing Names - Separating  - Last Name

# Identifying records with suffixes in each column and appending to a new dataframe
# Here, we go through each column, search for a specific suffix, Title (Proper) case the names for the other columns (i.e. the ones that do not have the suffix), and then add them into a new dataframe. The new dataframe is basically the list of names with suffixes.
# np.where: We use this, instead of the basic str.title to exclude the columns with 1 characters. This is useful for MI columns. This is because, some the Last names can still have 1 character Middle Names within that column, not separately in the MI column.


mask_L1_II = (data['L1'].str.len() == 2) & (data['L1'].str.contains("II"))
x = data[mask_L1_II]
for i in one_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = x

mask_L2_II = (data['L2'].str.len() == 2) & (data['L2'].str.contains("II"))
x = data[mask_L2_II]
for i in two_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L3_II = (data['L3'].str.len() == 2) & (data['L3'].str.contains("II"))
x = data[mask_L3_II]
for i in three_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L4_II = (data['L4'].str.len() == 2) & (data['L4'].str.contains("II"))
x = data[mask_L4_II]
for i in four_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L5_II = (data['L5'].str.len() == 2) & (data['L5'].str.contains("II"))
x = data[mask_L5_II]
for i in five_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_L1_III = (data['L1'].str.len() == 3) & (data['L1'].str.contains("III"))
x = data[mask_L1_III]
for i in one_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L2_III = (data['L2'].str.len() == 3) & (data['L2'].str.contains("III"))
x = data[mask_L2_III]
for i in two_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L3_III = (data['L3'].str.len() == 3) & (data['L3'].str.contains("III"))
x = data[mask_L3_III]
for i in three_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L4_III = (data['L4'].str.len() == 3) & (data['L4'].str.contains("III"))
x = data[mask_L4_III]
for i in four_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L5_III = (data['L5'].str.len() == 3) & (data['L5'].str.contains("III"))
x = data[mask_L5_III]
for i in five_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_L1_IV = (data['L1'].str.len() == 2) & (data['L1'].str.contains("IV"))
x = data[mask_L1_IV]
for i in one_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L2_IV = (data['L2'].str.len() == 2) & (data['L2'].str.contains("IV"))
x = data[mask_L2_IV]
for i in two_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L3_IV = (data['L3'].str.len() == 2) & (data['L3'].str.contains("IV"))
x = data[mask_L3_IV]
for i in three_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L4_IV = (data['L4'].str.len() == 2) & (data['L4'].str.contains("IV"))
x = data[mask_L4_IV]
for i in four_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L5_IV = (data['L5'].str.len() == 2) & (data['L5'].str.contains("IV"))
x = data[mask_L5_IV]
for i in five_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_L1_JR = (data['L1'].str.len() == 2) & (data['L1'].str.contains("JR"))
x = data[mask_L1_JR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])                                                #Because JR and SR should also be title case
suf_name = suf_name.append(x)

mask_L2_JR = (data['L2'].str.len() == 2) & (data['L2'].str.contains("JR"))
x = data[mask_L2_JR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)
                     
mask_L3_JR = (data['L3'].str.len() == 2) & (data['L3'].str.contains("JR"))
x = data[mask_L3_JR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L4_JR = (data['L4'].str.len() == 2) & (data['L4'].str.contains("JR"))
x = data[mask_L4_JR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L5_JR = (data['L5'].str.len() == 2) & (data['L5'].str.contains("JR"))
x = data[mask_L5_JR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_L1_SR = (data['L1'].str.len() == 2) & (data['L1'].str.contains("SR"))
x = data[mask_L1_SR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L2_SR = (data['L2'].str.len() == 2) & (data['L2'].str.contains("SR"))
x = data[mask_L2_SR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L3_SR = (data['L3'].str.len() == 2) & (data['L3'].str.contains("SR"))
x = data[mask_L3_SR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L4_SR = (data['L4'].str.len() == 2) & (data['L4'].str.contains("SR"))
x = data[mask_L4_SR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_L5_SR = (data['L5'].str.len() == 2) & (data['L5'].str.contains("SR"))
x = data[mask_L5_SR]
for i in full_l:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


#%%

# Separating Suffixes
# The code below is not required for datasets with suffixes in the same column. But it is useful when suffixes are in different columns. Mind the sequence. (It's Jr, Sr, II, III, IV, VI, I, V)
# The code below has been updated compared to previous versions, to make it more simple.


suf_name['Suffix'] = pd.np.where(suf_name['L1'] == "Jr", "Jr",
                                pd.np.where(suf_name['L2'] == "Jr", "Jr",
                                pd.np.where(suf_name['L3'] == "Jr", "Jr",
                                pd.np.where(suf_name['L4'] == "Jr", "Jr",
                                pd.np.where(suf_name['L5'] == "Jr", "Jr",
                                pd.np.where(suf_name['L1'] == "Sr", "Sr",
                                pd.np.where(suf_name['L2'] == "Sr", "Sr",
                                pd.np.where(suf_name['L3'] == "Sr", "Sr",
                                pd.np.where(suf_name['L4'] == "Sr", "Sr",
                                pd.np.where(suf_name['L5'] == "Sr", "Sr",
                                pd.np.where(suf_name['L1'] == "II", "II",
                                pd.np.where(suf_name['L2'] == "II", "II",
                                pd.np.where(suf_name['L3'] == "II", "II",
                                pd.np.where(suf_name['L4'] == "II", "II",
                                pd.np.where(suf_name['L5'] == "II", "II",
                                pd.np.where(suf_name['L1'] == "III", "III",
                                pd.np.where(suf_name['L2'] == "III", "III",
                                pd.np.where(suf_name['L3'] == "III", "III",
                                pd.np.where(suf_name['L4'] == "III", "III",
                                pd.np.where(suf_name['L5'] == "III", "III",
                                pd.np.where(suf_name['L1'] == "IV", "IV",
                                pd.np.where(suf_name['L2'] == "IV", "IV",
                                pd.np.where(suf_name['L3'] == "IV", "IV",
                                pd.np.where(suf_name['L4'] == "IV", "IV",
                                pd.np.where(suf_name['L5'] == "IV", "IV", 
                                None)))))))))))))))))))))))))

#%%
# Now we replace the suffixes within the columns that have suffixes. Again, this coding is not required for for datasets with suffixes in the same column, but useful when they are in different columns.

for i in full_l:
    suf_name.loc[(suf_name[i] == "Jr"), i] = None
    suf_name.loc[(suf_name[i] == "Sr"), i] = None
    suf_name.loc[(suf_name[i] == "II"), i] = None
    suf_name.loc[(suf_name[i] == "III"), i] = None
    suf_name.loc[(suf_name[i] == "IV"), i] = None


#%% Creating Whole Names for the Last Names with Suffix - Last Name

## Title Case (Proper) First Name Column
suf_name["First Name"] = suf_name["First Name"].str.title()
suf_name["MI"] = suf_name["MI"].str.title()
## Joining
suf_name["WholeName"] = suf_name["L1"].fillna('') + " " + suf_name["L2"].fillna('') + " " + suf_name["L3"].fillna('') + " " + suf_name["L4"].fillna('') + " " + suf_name["L5"].fillna('') + ", " + suf_name["First Name"].fillna('') + " " + suf_name["MI"].fillna('') + ", " + suf_name["Suffix"].fillna('')

suf_name_l = suf_name.copy()


#%% Fixing Names - Separating Suffixes - First Name

# First we identify suffixes in First Names
# For this dataset there are suffixes upto III in First Name column.

# First we check the number of columns it will split into. 
z = data["First Name"].str.split(" ", expand=True)

data[["F1","F2","F3"]] = data["First Name"].str.split(" ", expand=True)

full_f = ["F1","F2","F3"]
one_f = ["F2","F3"]
two_f = ["F1","F3"]
three_f = ["F1","F2"]


#%% Fixing Names - Separating  - First Name

# Identifying records with suffixes in each column and appending to a new dataframe
# Here, we go through each column, search for a specific suffix, Title (Proper) case the names for the other columns (i.e. the ones that do not have the suffix), and then add them into a new dataframe. The new dataframe is basically the list of names with suffixes.
# np.where: We use this, instead of the basic str.title to exclude the columns with 1 characters. This is useful for MI columns. This is because, some the First names can still have 1 character Middle Names within that column, not separately in the MI column.


mask_F1_II = (data['F1'].str.len() == 2) & (data['F1'].str.contains("II"))
x = data[mask_F1_II]
for i in one_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])                    # Character size != 1 means we are Title casing all words that are more than one letters
suf_name = x

mask_F2_II = (data['F2'].str.len() == 2) & (data['F2'].str.contains("II"))
x = data[mask_F2_II]
for i in two_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_F3_II = (data['F3'].str.len() == 2) & (data['F3'].str.contains("II"))
x = data[mask_F3_II]
for i in three_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_F1_III = (data['F1'].str.len() == 3) & (data['F1'].str.contains("III"))
x = data[mask_F1_III]
for i in one_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_F2_III = (data['F2'].str.len() == 3) & (data['F2'].str.contains("III"))
x = data[mask_F2_III]
for i in two_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_F3_III = (data['F3'].str.len() == 3) & (data['F3'].str.contains("III"))
x = data[mask_F3_III]
for i in three_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_F1_JR = (data['F1'].str.len() == 2) & (data['F1'].str.contains("JR"))
x = data[mask_F1_JR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])                                                #Because JR and SR should also be title case
suf_name = suf_name.append(x)

mask_F2_JR = (data['F2'].str.len() == 2) & (data['F2'].str.contains("JR"))
x = data[mask_F2_JR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)
                     
mask_F3_JR = (data['F3'].str.len() == 2) & (data['F3'].str.contains("JR"))
x = data[mask_F3_JR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_F1_SR = (data['F1'].str.len() == 2) & (data['F1'].str.contains("SR"))
x = data[mask_F1_SR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_F2_SR = (data['F2'].str.len() == 2) & (data['F2'].str.contains("SR"))
x = data[mask_F2_SR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_F3_SR = (data['F3'].str.len() == 2) & (data['F3'].str.contains("SR"))
x = data[mask_F3_SR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


#%%

# Separating Suffixes
# The code below is not required for datasets with suffixes in the same column. But it is useful when suffixes are in different columns. Mind the sequence. (It's Jr, Sr, II, III, IV, VI, I, V)
# The code below has been updated compared to previous versions, to make it more simple.


suf_name['Suffix'] = pd.np.where(suf_name['F1'] == "Jr", "Jr",
                                pd.np.where(suf_name['F2'] == "Jr", "Jr",
                                pd.np.where(suf_name['F3'] == "Jr", "Jr",
                                pd.np.where(suf_name['F1'] == "Sr", "Sr",
                                pd.np.where(suf_name['F2'] == "Sr", "Sr",
                                pd.np.where(suf_name['F3'] == "Sr", "Sr",
                                pd.np.where(suf_name['F1'] == "II", "II",
                                pd.np.where(suf_name['F2'] == "II", "II",
                                pd.np.where(suf_name['F3'] == "II", "II",
                                pd.np.where(suf_name['F1'] == "III", "III",
                                pd.np.where(suf_name['F2'] == "III", "III",
                                pd.np.where(suf_name['F3'] == "III", "III",
                                None))))))))))))


#%%
# Now we replace the suffixes within the columns that have suffixes. Again, this coding is not required for for datasets with suffixes in the same column, but useful when they are in different columns.

for i in full_f:
    suf_name.loc[(suf_name[i] == "Jr"), i] = None
    suf_name.loc[(suf_name[i] == "Sr"), i] = None
    suf_name.loc[(suf_name[i] == "II"), i] = None
    suf_name.loc[(suf_name[i] == "III"), i] = None
    
#%% Creating Whole Names for the First Names with Suffix - First Name


## Title Case (Proper) Last Name Column
suf_name["Last Name"] = suf_name["Last Name"].str.title()
suf_name["MI"] = suf_name["MI"].str.title()

## Joining
suf_name["WholeName"] = suf_name["Last Name"].fillna('') + ", " + suf_name["F1"].fillna('') + " " + suf_name["F2"].fillna('') + " " + suf_name["F3"].fillna('') + " " + suf_name["MI"].fillna('') + ", " + suf_name["Suffix"].fillna('')

suf_name_f = suf_name.copy()



#%% Fixing Names - Separating Suffixes - Middle Name

# First we identify suffixes in Middle Names
# For this dataset there are suffixes upto III in Middle Name column.

# First we check the number of columns it will split into. 
z = data["MI"].str.split(" ", expand=True)

data['MI'] = data["MI"].str.replace("STATE OF NY THE NYS","")


data[["M1","M2","M3"]] = data["MI"].str.split(" ", expand=True)

full_f = ["M1","M2","M3"]
one_f = ["M2","M3"]
two_f = ["M1","M3"]
three_f = ["M1","M2"]

#%% Fixing Names - Separating  - Middle Name


mask_M1_II = (data['M1'].str.len() == 2) & (data['M1'].str.contains("II"))
x = data[mask_M1_II]
for i in one_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])                    # Character size != 1 means we are Title casing all words that are more than one letters
suf_name = x

mask_M2_II = (data['M2'].str.len() == 2) & (data['M2'].str.contains("II"))
x = data[mask_M2_II]
for i in two_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_M3_II = (data['M3'].str.len() == 2) & (data['M3'].str.contains("II"))
x = data[mask_M3_II]
for i in three_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_M1_III = (data['M1'].str.len() == 3) & (data['M1'].str.contains("III"))
x = data[mask_M1_III]
for i in one_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_M2_III = (data['M2'].str.len() == 3) & (data['M2'].str.contains("III"))
x = data[mask_M2_III]
for i in two_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_M3_III = (data['M3'].str.len() == 3) & (data['M3'].str.contains("III"))
x = data[mask_M3_III]
for i in three_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_M1_JR = (data['M1'].str.len() == 2) & (data['M1'].str.contains("JR"))
x = data[mask_M1_JR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])                                                #Because JR and SR should also be title case
suf_name = suf_name.append(x)

mask_M2_JR = (data['M2'].str.len() == 2) & (data['M2'].str.contains("JR"))
x = data[mask_M2_JR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)
                     
mask_M3_JR = (data['M3'].str.len() == 2) & (data['M3'].str.contains("JR"))
x = data[mask_M3_JR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)


mask_M1_SR = (data['M1'].str.len() == 2) & (data['M1'].str.contains("SR"))
x = data[mask_M1_SR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_M2_SR = (data['M2'].str.len() == 2) & (data['M2'].str.contains("SR"))
x = data[mask_M2_SR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

mask_M3_SR = (data['M3'].str.len() == 2) & (data['M3'].str.contains("SR"))
x = data[mask_M3_SR]
for i in full_f:
    x[i] = np.where(x[i].str.len() != 1, x[i].str.title(), x[i])
suf_name = suf_name.append(x)

#%%

# Separating Suffixes


suf_name['Suffix'] = pd.np.where(suf_name['M1'] == "Jr", "Jr",
                                pd.np.where(suf_name['M2'] == "Jr", "Jr",
                                pd.np.where(suf_name['M3'] == "Jr", "Jr",
                                pd.np.where(suf_name['M1'] == "Sr", "Sr",
                                pd.np.where(suf_name['M2'] == "Sr", "Sr",
                                pd.np.where(suf_name['M3'] == "Sr", "Sr",
                                pd.np.where(suf_name['M1'] == "II", "II",
                                pd.np.where(suf_name['M2'] == "II", "II",
                                pd.np.where(suf_name['M3'] == "II", "II",
                                pd.np.where(suf_name['M1'] == "III", "III",
                                pd.np.where(suf_name['M2'] == "III", "III",
                                pd.np.where(suf_name['M3'] == "III", "III",
                                None))))))))))))

#%%
# Now we replace the suffixes within the columns that have suffixes. Again, this coding is not required for for datasets with suffixes in the same column, but useful when they are in different columns.

for i in full_f:
    suf_name.loc[(suf_name[i] == "Jr"), i] = None
    suf_name.loc[(suf_name[i] == "Sr"), i] = None
    suf_name.loc[(suf_name[i] == "II"), i] = None
    suf_name.loc[(suf_name[i] == "III"), i] = None
    
#%% Creating Whole Names for the First Names with Suffix - Middle Name


## Title Case (Proper) First Name Column
suf_name["Last Name"] = suf_name["Last Name"].str.title()
suf_name["First Name"] = suf_name["First Name"].str.title()

## Joining
suf_name["WholeName"] = suf_name["Last Name"].fillna('') + ", " + suf_name["First Name"].fillna('') + suf_name["M1"].fillna('') + " " + suf_name["M2"].fillna('') + " " + suf_name["M3"].fillna('') + ", " + suf_name["Suffix"].fillna('')


suf_name_m = suf_name.copy()


#%% Formatting Whole Names in Suffix Names Tables

# Removing double spacing - Run this multiple times to remove all more than double spaces    

for _ in range(3):
    suf_name_l["WholeName"] = suf_name_l["WholeName"].str.replace("  "," ")                      
for _ in range(3):
    suf_name_f["WholeName"] = suf_name_f["WholeName"].str.replace("  "," ")
for _ in range(3):
    suf_name_m["WholeName"] = suf_name_m["WholeName"].str.replace("  "," ")                 

# Replacing " ,"
suf_name_l["WholeName"] = suf_name_l["WholeName"].str.replace(" ,",",")                      
suf_name_f["WholeName"] = suf_name_f["WholeName"].str.replace(" ,",",")
suf_name_m["WholeName"] = suf_name_m["WholeName"].str.replace(" ,",",")  

#%% Combining Suffix Data with Non-Suffix data

# First, Combining (Appending) the Last Name Suffixes and First name suffixes
suf_name = pd.concat([suf_name_l, suf_name_f, suf_name_m])

# Replace the nans with None
suf_name = suf_name.replace({np.nan: None})

# Formatting the non-suffix data
# Before combining with the rest of the data without the suffixes, we will also title case the names in the non-suffix data

index_list = list(suf_name.index.values)
non_suf_name = data.drop(data.index[index_list])

    
# Joining Back names - We do need to join separately (from the su names) as joining together will leave the non suffix names as "James, Murray, "
## Title Case (Proper) First Name and Last Name Column

non_suf_name["WholeName"] = non_suf_name["Last Name"].str.title().fillna('') + ', ' + non_suf_name["First Name"].str.title().fillna('') + ' ' + non_suf_name["MI"].str.title().fillna('')

# combining 

data_name = pd.concat([suf_name,non_suf_name])

# Cleaning the Whole Name columns
data_name["WholeName"] = data_name["WholeName"].str.replace(" ,",",")
data_name["WholeName"] = data_name["WholeName"].str.strip() 
for _ in range(3):
    data_name["WholeName"] = data_name["WholeName"].str.replace("  "," ")

#%% Matching branch

match = pd.read_excel('NYSLRS(actives)_MatchFile.xlsx', sheet_name = 'Master-Branch')

data_name_branch = data_name.merge(match, how = 'left', left_on = 'EMPLOYER_NAME', right_on = 'Original Employer Name')

## At this point, convert the data to excel, check for the empty branches (i.e. new) employers, update the match file with their respective branches, and run the above match again to check that all the data points have a branch name.


#%% Other Cleaning

keep = ['EMPLID','RET_SYSTEM', 'EARNINGS', 'LOCATION_CODE','EMPLOYER_NAME', 'JOB_CODE', 'JOB_CODE_DESCRIPTION','DATE_OF_MEMBERSHIP','WholeName','BranchName']

data_name_branch = data_name_branch[keep]

data_name_branch["DATE_OF_MEMBERSHIP"] = pd.to_datetime(data_name_branch["DATE_OF_MEMBERSHIP"]).dt.date

data_name_branch["PayBasis"] = 'NDR'
data_name_branch["Rate"] = 'NDR'
data_name_branch["PayYear"] = '2024'

#%% Separation - Municipalities

# First we update the agncy name and branch names for municipalities.

match2 = pd.read_excel('NYSLRS(actives)_MatchFile.xlsx', sheet_name = 'Master-Agency', dtype = str)

data_name_branch_muniagency = data_name_branch.merge(match2, how = 'left', left_on = 'LOCATION_CODE', right_on = 'Location Code')

## At this point, save this dataframe and check if there are any new municipalities that need to be added to the match file. Use BranchName_x and Branchname_y in combination to find the blank (i.e. the new municipality codes)

# Extracting the municipalities

keep2 = ['Cities','Counties','Villages','Towns']

data_muni = data_name_branch_muniagency[data_name_branch_muniagency['BranchName_y'].isin(keep2)]

data_muni['SubAgencyName'] = pd.np.where(data_muni['RET_SYSTEM'] == "ERS", "NYSLRS - General Employee",
                                         pd.np.where(data_muni['RET_SYSTEM'] == "PFRS", "NYSLRS - Police & Fire", None))

col_keep = ['BranchName_y', 'AgencyName', 'SubAgencyName', 'WholeName', 'JOB_CODE_DESCRIPTION', 'PayBasis', 'Rate', 'EARNINGS', 'PayYear','DATE_OF_MEMBERSHIP',
            'RET_SYSTEM', 'LOCATION_CODE', 'EMPLOYER_NAME', 'JOB_CODE', 'EMPLID']

data_muni = data_muni[col_keep]

col_rename = {'BranchName_y' : 'BranchName',
              'AgencyName' : 'AgencyName',
              'SubAgencyName' : 'SubAgencyName',
              'WholeName' : 'WholeName',
              'JOB_CODE_DESCRIPTION' : 'PositionName',
              'PayBasis' : 'PayBasis',
              'Rate' : 'Rate',
              'EARNINGS' : 'YTDPay',
              'PayYear' : 'PayYear',
              'DATE_OF_MEMBERSHIP' : 'HireDate',
              'EMPLID' : 'EmployeeID'}

data_muni = data_muni.rename(columns=col_rename)

counties = data_muni[data_muni["BranchName"] == 'Counties']
towns = data_muni[data_muni["BranchName"] == 'Towns']
villages = data_muni[data_muni["BranchName"] == 'Villages']
cities = data_muni[data_muni["BranchName"] == 'Cities']

## Saving to respective municipality docs

counties.to_csv("FormattedFile_2024_NYSLRS_Payrolls_Counties_8.12.24.csv", index = False)
towns.to_csv("FormattedFile_2024_NYSLRS_Payrolls_Towns_8.12.24.csv", index = False)
villages.to_csv("FormattedFile_2024_NYSLRS_Payrolls_Villages_8.12.24.csv", index = False)
cities.to_csv("FormattedFile_2024_NYSLRS_Payrolls_Cities_8.12.24.csv", index = False)

#%% Separation - Schools

data_schools = data_name_branch_muniagency[data_name_branch_muniagency['BranchName_x'] == 'Schools']

col_keep_schools = ['BranchName_x', 'WholeName', 'JOB_CODE_DESCRIPTION', 'PayBasis', 'Rate', 'EARNINGS', 'PayYear','DATE_OF_MEMBERSHIP',
            'RET_SYSTEM', 'LOCATION_CODE', 'EMPLOYER_NAME', 'JOB_CODE', 'EMPLID']

data_schools = data_schools[col_keep_schools]

# Removing School Board Associations

rem_schools = ['NYS SCHOOL BD ASSOCIATION', 
               'CENTRAL NY SCHOOL BDS ASSOC', 
               'ERIE CO ASSOC SCH BD']

for i in rem_schools:
    data_schools = data_schools[data_schools['EMPLOYER_NAME'] != i]


## Saving to school file

data_schools.to_csv("FormattedFile_2024_NYSLRS_Payrolls_Schools_8.12.24.csv", index = False)

#%% Separation - Housing Authorities

data_housauth = data_name_branch_muniagency[data_name_branch_muniagency['BranchName_x'] == 'Housing Authority']

match3 = pd.read_excel('NYSLRS(actives)_MatchFile.xlsx', sheet_name = 'Housing Authorities', dtype = str)

data_housauth = data_housauth.merge(match3, how = 'left', left_on = 'EMPLOYER_NAME', right_on = 'Original Name')

## At this point save the file to check if there are any new housing authorities


col_keep_houseauth = ['BranchName', 'AgencyName_y', 'SubAgencyName', 'WholeName', 'JOB_CODE_DESCRIPTION', 'EARNINGS' , 'PayYear', 'PayBasis', 'Rate', 'DATE_OF_MEMBERSHIP',
                      'RET_SYSTEM', 'LOCATION_CODE', 'JOB_CODE', 'EMPLID']

data_housauth = data_housauth[col_keep_houseauth]

col_rename = {'BranchName' : 'BranchName',
              'AgencyName_y' : 'AgencyName',
              'SubAgencyName' : 'SubAgencyName',
              'WholeName' : 'WholeName',
              'JOB_CODE_DESCRIPTION' : 'PositionName',
              'PayBasis' : 'PayBasis',
              'Rate' : 'Rate',
              'EARNINGS' : 'YTDPay',
              'PayYear' : 'PayYear',
              'DATE_OF_MEMBERSHIP' : 'HireDate',
              'EMPLID' : 'EmployeeID'}

data_housauth = data_housauth.rename(columns=col_rename)

## Saving to Housing Authority file

data_housauth.to_csv("FormattedFile_2024_NYSLRS_Payrolls_HousingAuthorities_8.12.24.csv", index = False)

#%% Special Districts

spd = ['Fire & Water', 'Libraries', 'Parks', 'Police & Fire', 'Sanitation', 'Sewer', 'Water']

data_spd = data_name_branch_muniagency[data_name_branch_muniagency['BranchName_x'].isin(spd)]


## Preparing the dataframe column for unique identifiers. The unique identifier for this dataset is a bit tricky as there are different ERS and PFRS employees for the same employer. 

data_spd['Ret N'] = pd.np.where(data_spd['RET_SYSTEM'] == "ERS", "1",
                                pd.np.where(data_spd['RET_SYSTEM'] == "PFRS", "2", None))

data_spd['Employer Name_Ret N'] = data_spd['EMPLOYER_NAME'] + " - " + data_spd['Ret N'].astype(str)

## Now Matching

match4 = pd.read_excel('NYSLRS(actives)_MatchFile.xlsx', sheet_name = 'Sp. Districts', dtype = str)

data_spd = data_spd.merge(match4, how = 'left', left_on = 'Employer Name_Ret N', right_on = 'Original Name (With retirement system #)')

## At this point save the file to check if there are any new Employers. Update match file as required.

data_spd['BranchName'] = 'Special Districts'

col_keep_spd = ['BranchName','BranchName_x', 'Master Special Districts SubAgency List', 'WholeName', 'JOB_CODE_DESCRIPTION', 'PayBasis', 'Rate', 'EARNINGS', 'PayYear','DATE_OF_MEMBERSHIP',
               'RET_SYSTEM', 'LOCATION_CODE', 'EMPLOYER_NAME', 'JOB_CODE', 'EMPLID' ]

data_spd = data_spd[col_keep_spd]

col_rename = {'BranchName' : 'BranchName',
              'BranchName_x' : 'AgencyName',
              'Master Special Districts SubAgency List' : 'SubAgencyName',
              'WholeName' : 'WholeName',
              'JOB_CODE_DESCRIPTION' : 'PositionName',
              'PayBasis' : 'PayBasis',
              'Rate' : 'Rate',
              'EARNINGS' : 'YTDPay',
              'PayYear' : 'PayYear',
              'DATE_OF_MEMBERSHIP' : 'HireDate',
              'EMPLID' : 'EmployeeID'}

data_spd = data_spd.rename(columns=col_rename)

## Saving to Housing Special Districts file

data_spd.to_csv("FormattedFile_2024_NYSLRS_Payrolls_SpecialDistricts_8.12.24.csv", index = False)


#%% Others - Removed Items


rem = ['State - Executive', 'State - Legislative', 'Z - Unknown', 'Public Authorities', 'Counties - Community College', 'Special' ]

data_rem = data_name_branch_muniagency[data_name_branch_muniagency['BranchName_x'].isin(rem)]

col_keep_rem = ['BranchName_x', 'WholeName', 'JOB_CODE_DESCRIPTION', 'PayBasis', 'Rate', 'EARNINGS', 'PayYear','DATE_OF_MEMBERSHIP',
            'RET_SYSTEM', 'LOCATION_CODE', 'EMPLOYER_NAME', 'JOB_CODE', 'EMPLID']

data_rem = data_rem[col_keep_rem]

data_rem.to_csv("FormattedFile_2024_NYSLRS_Payrolls_RemovedData_8.12.24.csv", index = False)


#%% Combining Municipalities and special districts for further analysis


analysis_file = pd.concat([counties,towns,villages,cities,data_spd], ignore_index=True)

analysis_file.to_excel("FormattedAnalysisFile_2024_NYSLRS_Payrolls_8.12.24.xlsx", index = False)



#%%

x = data_name_branch_muniagency[data_name_branch_muniagency['BranchName_x'] == 'Police & Fire']

data_spd.to_excel('y.xlsx',index = False)
data_spd.columns
data_muni['BranchName'].value_counts()
data_name_branch_muniagency['BranchName_x'].value_counts()
data_spd['YTDPay'].describe()

data_spd.to_excel('x.xlsx', index = False)




