import pandas as pd
import math
import numpy as np
import tabulate
import pprint

data = pd.read_excel("PAT appt by SURGERY TYPE.xlsx")

########################## PAT BY SURGERY TYPE

######## Data cleaning and standardizing
data = data.drop(['Visit Type NM'], axis=1)
data = data.dropna()
data = data.reset_index(drop=True)
for x in range(len(data["Surgery Case"])):
    data["Surgery Case"][x] = data["Surgery Case"][x].split(",")[0]

######## Print the 10 surgery types with highest average PAT cycle times
worst10Cycles = data.groupby(["Surgery Case"]).agg({'Avg. Cycle Time Minutes': ['mean'], 'Number of Records': ['sum']}).sort_values(('Avg. Cycle Time Minutes', 'mean'), ascending=False).head(10)
print("The 10 Worst Cycle Times by Surgery Type are: ", worst10Cycles)

######## Print the 10 surgery types with lowest average PAT cycle times
top10Cycles = data.groupby(["Surgery Case"]).agg({'Avg. Cycle Time Minutes': ['mean'], 'Number of Records': ['sum']}).sort_values(('Avg. Cycle Time Minutes', 'mean'), ascending=True).head(10)
# print("The 10 Best Cycle Times by Surgery Type are: ", top10Cycles)
print(tabulate(top10Cycles, headers='keys', tablefmt='psql'))

######## 10 Surgery types performed the most last year
mostPerformed = data.groupby(["Surgery Case"]).agg({'Avg. Cycle Time Minutes': ['mean'], 'Number of Records': ['sum']}).sort_values(('Number of Records', 'sum'), ascending=False).head(10)
print("The 10 Most Performed Surgeries Last Year Were: ", mostPerformed)

######## % of total PAT appts under 60min
x = data.groupby(by=["Surgery Case"]).mean().sort_values('Avg. Cycle Time Minutes', ascending=True)

data['Appt Meeting 60min Goal?'] = "No"
for entry in range(len(data)):
    # print(data['Avg. Cycle Time Minutes'][entry])
    if data['Avg. Cycle Time Minutes'][entry] <= 60:
        data['Appt Meeting 60min Goal?'][entry] = "Yes"

print("Number of appts under 60 min: ", data.loc[data["Appt Meeting 60min Goal?"] == "Yes"]["Number of Records"].sum())
print("Number of appts over 60 min: ", data.loc[data["Appt Meeting 60min Goal?"] == "No"]["Number of Records"].sum())
print("Percentage of PAT appts under 60 minutes in 2021: " 
    + str(round(data.loc[data["Appt Meeting 60min Goal?"] == "Yes"]["Number of Records"].sum() 
        / data.loc[data["Appt Meeting 60min Goal?"] == "No"]["Number of Records"].sum() * 100, 3)) + "%")

