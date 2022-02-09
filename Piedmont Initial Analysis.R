setwd("/Users/christinacollins/Documents/Senior Design")
install.packages("readxl")
library("readxl")
read_excel("Piedmont Current.xlsx")
mydata = read_excel("Piedmont Current.xlsx")

mydata = read.csv("Official Data.csv")
attach(mydata)

library(chron)
library(dplyr)
mydata %>%
  mutate(Arrival.Interval = hours(times(Arrival.Interval)))
hr = strptime(mydata$Appt.Interval, format = "%H:%M:%S")
mydata$hr = hr

library(chron)
tms = times(format(hr, "%H:%M:%S"))
head(tms)
mydata$tms = tms

#Appt. Time vs. Avg. Cycle Time
ggplot(mydata, aes(x = (factor(tms)), y = Avg..Cycle.Time.Minutes)) + 
  stat_summary(fun = "mean", geom = "bar") + 
  theme(axis.text.x=element_text(angle = 45)) +
  xlab("Appt. Time") + ylab("Avg. Cycle Time (Mins)") + 
  ggtitle("Appt. Time vs. Avg. Cycle Time (Mins)")


#Appt. Time vs. Avg. Time to Room
ggplot(mydata, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes)) + 
  stat_summary(fun = "mean", geom = "bar") + 
  theme(axis.text.x=element_text(angle = 45)) +
  xlab("Appt. Time") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Appt. Time vs. Avg. Time to Room (Mins)")

#Avg. Time to Room by Weekday
lvl_order = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
ggplot(mydata, aes(x = factor(Weekday, level = lvl_order), y = Avg..Time.To.Room.Minutes)) +
  stat_summary(fun = "mean", geom = "bar") +
  xlab("Weekday") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Avg. Time to Room (Mins) by Weekday")

#Appts per Weekday
ggplot(mydata, aes(Weekday)) + geom_bar() + 
  scale_x_discrete(limits = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")) +
  ggtitle("2021 Appointments per Day")

#attempt at boxplots (probably not helpful)
ggplot(mydata, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes)) + 
  stat_summary(fun = "mean") + 
  geom_boxplot() +
  theme(axis.text.x=element_text(angle = 45)) +
  xlab("Arrival Time") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Arrival Time vs. Avg. Time to Room (Mins)")

ggplot(mydata, aes(x = factor(Weekday, level = lvl_order), y = Avg..Time.To.Room.Minutes)) +
  stat_summary(fun = "mean") +
  geom_boxplot() +
  xlab("Weekday") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Avg. Time to Room (Mins) by Weekday")

#walk ins
walkins = mydata[mydata$Walk.in == "Yes",]

#walk-in arrival time vs. avg cycle time
ggplot(walkins, aes(x = (factor(tms)), y = Avg..Cycle.Time.Minutes)) + 
  stat_summary(fun = "mean", geom = "bar") + 
  theme(axis.text.x=element_text(angle = 45)) +
  xlab("Walk-in Time") + ylab("Avg. Cycle Time (Mins)") + 
  ggtitle("Walk-in Arrival Time vs. Avg. Cycle Time (Mins)")

#walk in time vs avg. time to room
ggplot(walkins, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes)) + 
  stat_summary(fun = "mean", geom = "bar") + 
  theme(axis.text.x=element_text(angle = 45)) +
  xlab("Walk-in Time") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Walk-in Time vs. Avg. Time to Room (Mins)") 

#avg time to room by weekday for walkins
lvl_order = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
ggplot(walkins, aes(x = factor(Weekday, level = lvl_order), y = Avg..Time.To.Room.Minutes)) +
  stat_summary(fun = "mean", geom = "bar") +
  xlab("Weekday") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Avg. Time to Room (Mins) by Weekday for Walk-ins") 

#walks ins per day 2021
ggplot(walkins, aes(Weekday)) + geom_bar() + 
  scale_x_discrete(limits = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")) +
  ggtitle("2021 Walk-ins per Day")

#wait time by mychart status
ggplot(mydata, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes, group = My.Chart.Status.NM, color = My.Chart.Status.NM)) +
  stat_summary(fun = "mean", geom = "line") +
  theme(legend.position = "bottom", axis.text.x=element_text(angle = 45))

#wait time by patient late or on time
ggplot(mydata, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes, group = Patient.Late, color = Patient.Late)) +
  stat_summary(fun = "mean", geom = "line") +
  theme(legend.position = "bottom", axis.text.x=element_text(angle = 45))

#wait time by walk in or not
ggplot(mydata, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes, group = Walk.in, color = Walk.in)) +
  stat_summary(fun = "mean", geom = "line") +
  theme(legend.position = "bottom", axis.text.x=element_text(angle = 45)) +
  xlab("Time") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Avg. Time to Room (Mins)") 

#wait time by weekday (view all)
gg = ggplot(mydata, aes(x = (factor(tms)), y = Avg..Time.To.Room.Minutes, group = Weekday, color = Weekday)) +
  stat_summary(fun = "mean", geom = "line") +
  theme(legend.position = "bottom", axis.text.x=element_text(angle = 45)) +
  xlab("Time") + ylab("Avg. Time to Room (Mins)") +
  ggtitle("Avg. Time to Room (Mins)")

gg + scale_color_hue(breaks = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")) 




