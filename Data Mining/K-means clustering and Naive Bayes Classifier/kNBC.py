from __future__ import division
import readData
import WordList
import TopWords
import csv
import os
import random
import numpy as np
import sys
import string
import scipy
import myKMeans
from sklearn.cluster import KMeans
from collections import Counter
from NaiveBayesClassifier import *
from sklearn.externals import joblib

dataTraining=[]
reviewListTotal=[]

def get_matrix(topWordList,posReviewList,negReviewList):
    Wp = [[0]*2500 for _ in xrange(2000)]
    Wnp = [[0]*2500 for _ in xrange(2000)]
    for i in range(0,len(topWordList)):
        word=topWordList[i]
        for k in range(0,len(posReviewList)):
            if word in posReviewList[k]:
                Wp[i][k]=Counter(posReviewList[k])[word]
            else:
                Wp[i][k]=0
    for i in range(0,len(topWordList)):
        word=topWordList[i]
        for k in range(0,len(negReviewList)):
            if word in negReviewList[k]:
                Wnp[i][k]=Counter(negReviewList[k])[word]
            else:
                Wnp[i][k]=0
    return Wp,Wnp

def getBinaryFeatures(positiveTopics,negetiveTopics):
    binaryFeatures = [[0]*100 for _ in xrange(5000)]
    for i in range(0,50):
        for k in range(0,5000):
            checkPresent=0
            for word in positiveTopics[i]:
                if(word in reviewListTotal[k]):
                    binaryFeatures[k][i]=1
                    checkPresent=1
                    break
            if checkPresent==0:
                binaryFeatures[k][i]=0
    for i in range(0,50):
        for k in range(0,5000):
            checkPresent=0
            for word in negetiveTopics[i]:
                if(word in reviewListTotal[k]):
                    binaryFeatures[k][i+50]=1
                    checkPresent=1
                    break
            if checkPresent==0:
                binaryFeatures[k][i+50]=0
    return binaryFeatures                        
                
def main():
    
    # reading the date
    global dataTraining
    global reviewListTotal
    filename="stars_data.csv"
    dataTraining=readData.getData(filename)
    
    
    wordListTotal=[]
    posReviewListTotal=[]
    negReviewListTotal=[]
    classLabels=[]
    # no of data
    noOfData=len(dataTraining)
    
    
    for i in range(0,noOfData):
        templist=WordList.getList(dataTraining[i][0])
        reviewListTotal.append(templist)
        wordListTotal.extend(templist)
        classLabels.append(dataTraining[i][1])
        if(dataTraining[i][1]==1):
            posReviewListTotal.append(templist)
        else:
            negReviewListTotal.append(templist)
    
    # get 2000 words ranked from 201 to 2200 in terms of frequency
    topWordList=TopWords.getList(wordListTotal)
    
    # get positive matrix and negetive matrix
    Wp,Wnp=get_matrix(topWordList,posReviewListTotal,negReviewListTotal)
    
    # convert to Wp and Wnp to matrix of type float    
    Wp=np.array(Wp, dtype=float)
    Wnp=np.array(Wnp, dtype=float)    
    
    noOfClusters=200
    # clustering positive matrix
    learnWp=myKMeans.getModel(Wp,noOfClusters)
    
    # clustering negetive matrix
    learnWnp=myKMeans.getModel(Wnp,noOfClusters)
    
    clusterDataWp=myKMeans.getClusterData(learnWp.labels_,topWordList,noOfClusters)
    clusterDataWnp=myKMeans.getClusterData(learnWnp.labels_,topWordList,noOfClusters)
    
    topWordList=joblib.load('topWordList.pkl')
    clusterDataWp=joblib.load('positiveSKTOPICS50.pkl')
    clusterDataWnp=joblib.load('negetiveSKTOPICS50.pkl')
    
    binaryFeatures=getBinaryFeatures(clusterDataWp,clusterDataWnp)
    topics=clusterDataWp+clusterDataWnp
    print "no of rows: ",len(binaryFeatures),"no of columns: ",len(binaryFeatures[0])
    print "no of features: ", len(topics)
    
    model=mynbc(binaryFeatures,classLabels,topics)
    model.fit()
    model.predict(reviewListTotal,classLabels)
    model.performance()

if __name__ == '__main__':
    main()
