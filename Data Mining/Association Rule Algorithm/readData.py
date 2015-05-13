import csv
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