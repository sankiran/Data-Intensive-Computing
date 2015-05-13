from __future__ import division
from collections import Counter


class mynbc:
    def __init__(self, binaryFeatures, classLabels,topics):
        self.binaryFeatures=binaryFeatures
        self.classLabels=classLabels
        self.topics=topics
        self.classLabel1Training=2+Counter(classLabels)[1]
        self.classLabel0Training=2+Counter(classLabels)[0]
        self.priorClassLabel1Training=self.classLabel1Training/(self.classLabel1Training+self.classLabel0Training)
        self.priorClassLabel0Training=self.classLabel0Training/(self.classLabel1Training+self.classLabel0Training)
        self.zeroOneLoss=0
        self.likelihood={}
        for i in range(0,len(self.binaryFeatures[0])):
            self.likelihood[i]=([1/self.classLabel1Training,1-(1/self.classLabel1Training),1/self.classLabel0Training,1-(1/self.classLabel0Training)])
        
    def fit(self):
        for i in range(0,len(self.binaryFeatures[0])):
            for k in range (0,len(self.binaryFeatures)):
                if self.binaryFeatures[k][i]==1:
                    if self.classLabels[k]==1:
                        self.likelihood[i][0]=((self.likelihood[i][0]*self.classLabel1Training)+1)/self.classLabel1Training
                        self.likelihood[i][1]=1-self.likelihood[i][0]
                    else:
                        self.likelihood[i][2]=((self.likelihood[i][2]*self.classLabel0Training)+1)/self.classLabel0Training
                        self.likelihood[i][3]=1-self.likelihood[i][2]
    def predictClass(self, sampleReveiw):
        posteriorClassLabel1=self.priorClassLabel1Training
        posteriorClassLabel0=self.priorClassLabel0Training
        for i in range(0, len(self.topics)):
            currentTopic=self.topics[i]
            checkTopic=0
            for word in currentTopic:
                if(word in sampleReveiw):
                    posteriorClassLabel1=posteriorClassLabel1*self.likelihood[i][0]
                    posteriorClassLabel0=posteriorClassLabel0*self.likelihood[i][2]
                    checkTopic=1
                    break          
            if checkTopic==0:
                posteriorClassLabel1=posteriorClassLabel1*self.likelihood[i][1]
                posteriorClassLabel0=posteriorClassLabel0*self.likelihood[i][3]
        classType=-1
        if(posteriorClassLabel1>posteriorClassLabel0):
            classType=1
        else:
            classType=0
        return classType
    
    def predict(self,testReviewList,testClassLabels):
        self.zeroOneLoss=0
        noOfRec=len(testReviewList)
        for i in range(0,noOfRec):
            classType=self.predictClass(testReviewList[i])
            if classType!=testClassLabels[i]:
                self.zeroOneLoss=self.zeroOneLoss+1
        
        self.zeroOneLoss=self.zeroOneLoss/noOfRec
    def performance(self):
        print "zero one loss : ",self.zeroOneLoss
    def getLoss(self):
        return self.zeroOneLoss