# =====================================================================
# CSE587
# Author: Sankiran Srinath
# Email: sankiran@buffalo.edu
# =====================================================================

# need to install the following two packages in CCR(at least)
# install.packages("forecast")
# install.packages("fpp")
# data path /gpfs/courses/cse587/spring2015/data/hw2/data
#ta path /Users/sankiran/Documents/Study/UB/Data Intensive Computing/Projects/DIC Project 2/data

library(forecast)
library(fpp)


# need to read the stocklist, and loop all files
### TO DO
#setwd("/Users/sankiran/Documents/Study/UB/Data Intensive Computing/Projects/DIC Project 2/data")
#ldf <- list() # creates a list
#listcsv <- dir(pattern = "*.csv") # creates the list of all the csv files in the directory
#for (k in 1:length(listcsv)) { 
 # ldf[[k]] <- read.csv(listcsv[k])
#}

path = "/gpfs/courses/cse587/spring2015/data/hw2/data"
file.names <- dir(path, pattern =".csv")
#print(file.names)
listArima = c()
listHW = c()
listLR = c()
listFileNames = c()

for(j in 1:length(file.names)){
  filenames = paste(path, file.names[j], sep = "/")

# just read one file
#filename = "/gpfs/courses/cse587/spring2015/data/hw2/data/AAPL.csv"
#filename = "/Users/sankiran/Documents/Study/UB/Data_Intensive_Computing/Projects/DIC_Project_2/data/"

# if file is not empty
if(file.info(filenames)[1]>0) {
  
  # read one csv file into variable (DO NOT EDIT)
  textData=read.csv(file=filenames, header=T)
  if(nrow(textData) == 754) {
  
  # convert txt data to time-series data, in day unit (DO NOT EDIT)
  tsData = ts(rev(textData$Adj.Close),start=c(2012, 1),frequency=365)
  
  # define train data (DO NOT EDIT)
  trainData = window(tsData, end=c(2014,14))
  
  # define test data (DO NOT EDIT)
  testData = window(tsData, start=c(2014,15))
             
  # MAE row vector (DO NOT EDIT)
  MAE = matrix(NA,1,length(testData))
  
  # MAE for Holt-Winters Model
  MAEHW = matrix(NA,1,length(testData))
  
  # MAE for Linear Regression Model
  MAELR = matrix(NA,1,length(testData))
  
  # apply ARIMA model (DO NOT EDIT)
  fitData = auto.arima(trainData,seasonal=FALSE,lambda=NULL,approximation=TRUE)
  
  # the other two models
  ### TO DO
  
  # Apply Holt-Winters Model
  fitDataHW = HoltWinters(trainData, gamma = FALSE)
  
  # Apply Linear Regression Model
  #y = ts(rnorm(120,0,3) + 1:120 + 20*sin(2*pi*(1:120)/12), frequency=12)
  fitLinRegn = tslm(trainData ~ trend + season)
  
  # apply forecast(DO NOT EDIT)
  forecastData = forecast(fitData, h=length(testData))
  
  #apply forecast for HW Model
  forecastDataHW = forecast(fitDataHW, h=length(testData))
  
  #apply forecast for HW Model
  forecastLinRegn = forecast(fitLinRegn, h=length(testData))
  
  # print variable and see what is in the result data set
  #print(forecastData)
  
  # print variable and see what is in the result data set for HW model.
  #print(forecastDataHW)
  
  # print variable and see what is in the result data set for LM model.
  #print(forecastLinRegn)
  
  # calculate Mean Absolute Error 
  for(i in 1:length(testData))
  {
    MAE[1,i] = abs(forecastData$mean[i] - testData[i])
  }
  
  # calculate Mean Absolute Error for HW model 
  for(i in 1:length(testData))
  {
    MAEHW[1,i] = abs(forecastDataHW$mean[i] - testData[i])
  }
  
  # calculate Mean Absolute Error for LM model
  for(i in 1:length(testData))
  {
    MAELR[1,i] = abs(forecastLinRegn$mean[i] - testData[i])
  }
  listArima = c(listArima, sum(MAE[1,1:10]))
  listHW = c(listHW, sum(MAEHW[1,1:10]))
  listLR = c(listLR, sum(MAELR[1,1:10]))
  listFileNames = c(listFileNames, file.names[j])
  }
  }
}

  # this is the result you need for stock AAPL
  #print(sum(MAE[1,1:10]))
  
  # this is the result you need for stock AAPL from HW model
  #print(sum(MAEHW[1,1:10]))
  
  # this is the result you need for stock AAPL from LM model
  #print(sum(MAELR[1,1:10]))

#print(listArima)
#listArima = sort(listArima)
#print(listArima[1:10])
#print(listHW)
#listHW = sort(listHW)
#print(listHW[1:10])
#print(listLR)
#listLR = sort(listLR)
#print(listLR[1:10])

dfArima = data.frame(listFileNames, listArima)
orderArima = dfArima[order(dfArima[,2]),]
print(orderArima[1:10,])

dfHW = data.frame(listFileNames, listHW)
orderHW = dfHW[order(dfHW[,2]),]
print(orderHW[1:10,])

dfLR = data.frame(listFileNames, listLR)
orderLR = dfLR[order(dfLR[,2]),]
print(orderLR[1:10,])

jpeg("arima.jpg")
# plot the top 10 minimum sum of MAE in 3 models respectively
plot(orderArima[1:10,2], col = "blue")
lines(orderArima[1:10,2], lw = 2, col = "red")
dev.off()
### TO DO

# Plotting the values for HW model.
jpeg("hw.jpg")
plot(orderHW[1:10,2], col = "green")
lines(orderHW[1:10,2], lw = 2, col = "black")
dev.off()
# Plotting the values for LM model.
jpeg("lm.jpg")
plot(orderLR[1:10,2], col = "pink")
lines(orderLR[1:10,2], lw = 2, col = "yellow")
dev.off()
