import csv
from random import shuffle
from sklearn.externals import joblib

def getData(filename):
    dataTraining=[]
    original = file(filename, 'rU')
    reader = csv.reader(original)
    next(reader,None)
    i=0
    
    for row in reader:
        dataTraining.append([])
        dataTraining[i].append(row[7])
        stars=int(row[6])
        label=0
        if(stars==5):
            label=1
        else:
            label=0
        dataTraining[i].append(label)
        i=i+1
    
    joblib.dump(dataTraining,  'dataTrain.pkl')
    return dataTraining

def KFoldSample(dataTraining):
    shuffle(dataTraining)
    sampleTrain={}
    sampleTest={}
    for i in range(0,10):
        sampleTrain[i]=[]
    for i in range(0,10):
        sampleTest[i]=dataTraining[500*i:500*(i+1)]
    
    for i in range(0,10):
        for k in range(0,5000):
            if k<500*i or k>=500*(i+1):
                sampleTrain[i].append(dataTraining[k])
    
    joblib.dump(sampleTrain,  'sampleTrain.pkl')
    joblib.dump(sampleTest,  'sampleTest.pkl')
    return sampleTrain, sampleTest 

     
def getSample(dataTraining,noOfSample):
    shuffle(dataTraining)
    return(dataTraining[0:noOfSample])    
