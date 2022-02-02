from audioop import avg
import pandas as pd
import math
import numpy as np
import datetime

timestamps = pd.read_excel("PAT Time Stamps.xlsx")

########################## PAT TIME STAMPS

######## Data cleaning and standardizing
def militarytime_convert(time, meridiem): 
      
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if meridiem == "AM" and time.split(":")[0] == "12":
        return "00" + ":" + time.split(":")[1] + ":" + time.split(":")[2]

    # No change for AM Times
    elif meridiem == "AM":
        return time
      
    # Checking if last two elements of time
    # is PM and first two elements are 12   
    elif meridiem == "PM" and time.split(":")[0] == "12":
        return time
          
    else:
          
        # add 12 to hours and remove PM
        return str(int(time.split(":")[0]) + 12)+ ":" + time.split(":")[1] + ":" + time.split(":")[2]
###########################################################

timestamps = timestamps.dropna()
timestamps = timestamps.reset_index(drop=True)

timestamps["AM or PM Start"] = "AM"
timestamps["Appt Date"] = 0
for x in range(len(timestamps["Surgery Case"])):
    # standardizing surgery types
    timestamps["Surgery Case"][x] = timestamps["Surgery Case"][x].split(",")[0]
    
    # appt date and start time
    timestamps["Appt Date"][x] = timestamps["Check In Time"][x].split(" ")[0]
    if (timestamps["Check In Time"][x].split(" ")[2] == "PM"):
        timestamps["AM or PM Start"][x] = "PM"
    timestamps["Check In Time"][x] = timestamps["Check In Time"][x].split(" ")[1]
    
    # interview start time
    intstart = timestamps["Patient Interview Started Time"][x].split(" ")[2]
    timestamps["Patient Interview Started Time"][x] = timestamps["Patient Interview Started Time"][x].split(" ")[1]

    # interview complete time
    intcomplete = timestamps["Patient Interview Completed Time"][x].split(" ")[2]
    timestamps["Patient Interview Completed Time"][x] = timestamps["Patient Interview Completed Time"][x].split(" ")[1]

    # check out time
    checkout = timestamps["Check Out Time"][x].split(" ")[2]
    timestamps["Check Out Time"][x] = timestamps["Check Out Time"][x].split(" ")[1]

    # converting everything to military standard time
    timestamps["Check In Time"][x] = militarytime_convert(timestamps["Check In Time"][x], timestamps["AM or PM Start"][x])
    timestamps["Patient Interview Started Time"][x] = militarytime_convert(timestamps["Patient Interview Started Time"][x], intstart)
    timestamps["Patient Interview Completed Time"][x] = militarytime_convert(timestamps["Patient Interview Completed Time"][x], intcomplete)
    timestamps["Check Out Time"][x] = militarytime_convert(timestamps["Check Out Time"][x], checkout)


timestamps['Weekday'] = pd.to_datetime(timestamps['Appt Date'], format="%m/%d/%Y").dt.day_name()

# print(timestamps.head())

# timestamps.to_excel (r'C:\Users\csing\Documents\GitHub\PiedmontDataAnalysis\PAT_timestamps.xlsx', index = False, header=True)

timestamps = pd.read_excel("PAT_timestamps.xlsx")

######## Defining new columns to add
timestamps["Avg. Time To Room Minutes"] = 0
timestamps["Avg. Time In Room Minutes"] = 0
timestamps["Avg. Cycle Time Minutes"] = 0

######## Filling in the new columns with correct values
removed_list = []
for x in range(len(timestamps)):
    # collecting the times and date
    checkin = datetime.time(int(timestamps.loc[x, "Check In Time"].split(":")[0]), 
        int(timestamps.loc[x, "Check In Time"].split(":")[1]), 
        int(timestamps.loc[x, "Check In Time"].split(":")[2]))

    interviewstart = datetime.time(int(timestamps.loc[x, "Patient Interview Started Time"].split(":")[0]), 
        int(timestamps.loc[x, "Patient Interview Started Time"].split(":")[1]), 
        int(timestamps.loc[x, "Patient Interview Started Time"].split(":")[2]))

    interviewend = datetime.time(int(timestamps.loc[x, "Patient Interview Completed Time"].split(":")[0]), 
        int(timestamps.loc[x, "Patient Interview Completed Time"].split(":")[1]), 
        int(timestamps.loc[x, "Patient Interview Completed Time"].split(":")[2]))

    checkout = datetime.time(int(timestamps.loc[x, "Check Out Time"].split(":")[0]), 
        int(timestamps.loc[x, "Check Out Time"].split(":")[1]), 
        int(timestamps.loc[x, "Check Out Time"].split(":")[2]))

    date = timestamps.loc[x, "Appt Date"]

    #creating combine objects 
    checkin = datetime.datetime.combine(datetime.date(int(date.split("/")[2]), int(date.split("/")[0]), int(date.split("/")[1])), checkin)
    interviewstart = datetime.datetime.combine(datetime.date(int(date.split("/")[2]), int(date.split("/")[0]), int(date.split("/")[1])), interviewstart)
    interviewend = datetime.datetime.combine(datetime.date(int(date.split("/")[2]), int(date.split("/")[0]), int(date.split("/")[1])), interviewend)
    checkout = datetime.datetime.combine(datetime.date(int(date.split("/")[2]), int(date.split("/")[0]), int(date.split("/")[1])), checkout)

    # get rid of incorrect time stamps
    if (interviewstart < checkin) or (checkout < interviewstart) or (interviewend < interviewstart): 
        # print(timestamps.loc[x])
        timestamps = timestamps.drop([x])
        removed_list.append(x)
        continue

    # getting the durations
    wait = str(interviewstart - checkin).split(":")
    appt = str(interviewend - interviewstart).split(":")
    cycle = str(interviewend - checkin).split(":")
    
    # get rid of unusually long appointments (overnight)
    if "day" in str(cycle[0]):
        # print(timestamps.loc[x])
        removed_list.append(x)
        timestamps = timestamps.drop([x])
        continue

    # converting time stamps to averages
    avgwaittime = 0
    avgwaittime += int(wait[0])*60
    avgwaittime += int(wait[1])
    avgwaittime += int(wait[2])/60

    avgappt = 0
    # print(timestamps.loc[x])
    avgappt += int(appt[0])*60
    avgappt += int(appt[1])
    avgappt += int(appt[2])/60

    avgcycletime = 0
    avgcycletime += int(cycle[0])*60
    avgcycletime += int(cycle[1])
    avgcycletime += int(cycle[2])/60

    # assigning avgs to the columns
    timestamps.loc[x, "Avg. Time To Room Minutes"] = round(avgwaittime, 3)
    timestamps.loc[x, "Avg. Time In Room Minutes"] = round(avgappt, 3)
    timestamps.loc[x, "Avg. Cycle Time Minutes"] = round(avgcycletime, 3)
    
timestamps = timestamps.reset_index(drop=True)
# print(timestamps.head(50))
timestamps = timestamps.drop(['Check Out Time'], axis=1)
timestamps.to_excel (r'C:\Users\csing\Documents\GitHub\PiedmontDataAnalysis\PAT_timestamps_edit.xlsx', index = False, header=True)


        
########################## AGGREGATE RESULTS
data = pd.read_excel("PAT_timestamps_edit.xlsx")

######## Print the 10 surgery types with highest average PAT cycle times
worst10Cycles = data.groupby(["Surgery Case"]).agg({'Avg. Cycle Time Minutes': ['mean'], 'Surgery Case': ['count']}).sort_values(('Avg. Cycle Time Minutes', 'mean'), ascending=False).head(10)
print("The 10 Worst Cycle Times by Surgery Type are: ", worst10Cycles)

######## Print the 10 surgery types with lowest average PAT cycle times
top10Cycles = data.groupby(["Surgery Case"]).agg({'Avg. Cycle Time Minutes': ['mean'], 'Surgery Case': ['count']}).sort_values(('Avg. Cycle Time Minutes', 'mean'), ascending=True).head(10)
print("The 10 Best Cycle Times by Surgery Type are: ", top10Cycles)

######## 10 Surgery types performed the most last year
mostPerformed = data.groupby(["Surgery Case"]).agg({'Avg. Cycle Time Minutes': ['mean'], 'Surgery Case': ['count']}).sort_values(('Surgery Case', 'count'), ascending=False).head(10)
print("The 10 Most Performed Surgeries Last Year Were: ", mostPerformed)

######## % of total PAT appts under 60min
data['Appt Meeting 60min Goal?'] = "No"
for entry in range(len(data)):
    if data['Avg. Cycle Time Minutes'][entry] <= 60:
        data['Appt Meeting 60min Goal?'][entry] = "Yes"

print("Number of appts under 60 min: ", data.loc[data["Appt Meeting 60min Goal?"] == "Yes"]['Surgery Case'].count())
print("Number of appts over 60 min: ", data.loc[data["Appt Meeting 60min Goal?"] == "No"]['Surgery Case'].count())
print("Percentage of PAT appts under 60 minutes in 2021: " 
    + str(round(data.loc[data["Appt Meeting 60min Goal?"] == "Yes"]['Surgery Case'].count() 
        / data.loc[data["Appt Meeting 60min Goal?"] == "No"]['Surgery Case'].count() * 100, 3)) + "%")

######## Cycle Time Analysis

print("Average Cycle Time for 2021 is: ", round(data["Avg. Cycle Time Minutes"].mean(), 3))
print("Min Cycle Time was: ", data["Avg. Cycle Time Minutes"].min())
print("Max Cycle Time was: ", data["Avg. Cycle Time Minutes"].max())

# print(removed_list)
# print(len(removed_list))
