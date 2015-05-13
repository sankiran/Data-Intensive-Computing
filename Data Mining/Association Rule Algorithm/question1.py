from __future__ import division
import readData
import WordList
import TopWords
import numpy as np
from collections import Counter
from sklearn.externals import joblib

dataTraining=[]
reviewListTotal=[]

def getBinaryFeatures(topWordList,classLabelP,classLabelN):
    binaryFeatures = [[0]*(len(topWordList)+2) for _ in xrange(len(reviewListTotal))]
    for i in range(0,len(topWordList)):
        word=topWordList[i]
        for k in range(0,(len(reviewListTotal))):
            if word in reviewListTotal[k]:
                binaryFeatures[k][i]=1
            else:
                binaryFeatures[k][i]=0
    binaryFeatures=np.array(binaryFeatures)
    binaryFeatures=binaryFeatures.transpose()
    binaryFeatures[2000]=classLabelP
    binaryFeatures[2001]=classLabelN
    
    binaryFeatures=binaryFeatures.transpose()
    binaryFeatures=binaryFeatures.tolist()
    
    return binaryFeatures                       

# get candidate set 1

def getCandidateSet1(tBinaryFeatures):
    candidateSet1List=[]
    candidateSet1Count=[]
    
    for i in range(0,len(tBinaryFeatures)):
        candidateSet1List.append(i)
        candidateSet1Count.append((Counter(tBinaryFeatures[i])[1]))
    return candidateSet1List,candidateSet1Count

# get frequent item set 1

def getFrequentSet1(candidateSet1List,candidateSet1Count):
    frequentSet1=[]
    frequentSet1Count=[]
    noOfFrequentItems=0
    noOfInFrequentItems=0
    for i in range(0,len(candidateSet1List)):
        support=candidateSet1Count[i]/5000
        if (support)>=0.03:
            frequentSet1.append(candidateSet1List[i])
            frequentSet1Count.append(candidateSet1Count[i])
            noOfFrequentItems=noOfFrequentItems+1
        else:
            noOfInFrequentItems=noOfInFrequentItems+1
    
    print "Total Candidate Item sets at Stage 1: ",len(candidateSet1List)," No of Frequent Items selected : ",noOfFrequentItems," No of InFrequent Items pruned : ",noOfInFrequentItems
    return frequentSet1,frequentSet1Count

# get candidate set 2

def getCandidateSet2(tBinaryFeatures,frequentSet1):
    candidateSet2List={}
    candidateSet2Count={}
    
    candidateListCount=0
    for i in range(0,(len(frequentSet1)-1)):
        for k in range(i+1,len(frequentSet1)):
            item1=frequentSet1[i]
            item2=frequentSet1[k]
            candidateSet2List[candidateListCount]=[item1,item2]
            item1List=tBinaryFeatures[item1]
            item2List=tBinaryFeatures[item2]
            totalList=item1List+item2List
            
            candidateSet2Count[candidateListCount]=Counter(totalList)[2]
            
            candidateListCount=candidateListCount+1
    return  candidateSet2List,candidateSet2Count    
    

# get frequent item set 2

def getFrequentSet2(candidateSet2List,candidateSet2Count):
    frequentSet2=[]
    frequentSet2Count=[]
    noOfFrequentItems=0
    noOfInFrequentItems=0
    
    for i in range(0,len(candidateSet2List)):
        support=candidateSet2Count[i]/5000
        if support>=0.03:
            frequentSet2.append(candidateSet2List[i])
            frequentSet2Count.append(candidateSet2Count[i])
            noOfFrequentItems=noOfFrequentItems+1
        else:
            noOfInFrequentItems=noOfInFrequentItems+1
            
    print "Total Candidate Item sets at Stage 2: ",len(candidateSet2List)," No of Frequent Items selected : ",noOfFrequentItems," No of InFrequent Items pruned : ",noOfInFrequentItems
    
    return frequentSet2, frequentSet2Count


# evaluate candidate set 3

def evalCandidateSet3(frequentSet2,candidateSet3List,candidateSet3Count):
    newCandidateSet3List={}
    newCandidateSet3Count={}
    newCount=0
    for i in range(0,len(candidateSet3List)):
        itemSet=candidateSet3List[i]
        set1=[itemSet[0],itemSet[1]]
        set2=[itemSet[0],itemSet[2]]
        set3=[itemSet[1],itemSet[2]]
        if (set1 in frequentSet2) and (set2 in frequentSet2) and (set3 in frequentSet2):
            newCandidateSet3List[newCount]=candidateSet3List[i]
            newCandidateSet3Count[newCount]=candidateSet3Count[i]
            newCount=newCount+1
    
    return newCandidateSet3List,newCandidateSet3Count
# get candidate set 3

def getCandidateSet3(tBinaryFeatures,frequentSet2):
    candidateSet3List={}
    candidateSet3Count={}
    candidateListCount=0
    noOfSelectedCandidateItems=0
    for i in range(0,len(frequentSet2)-1):
        set1=frequentSet2[i]
        for k in range(i+1,len(frequentSet2)):
            set2=frequentSet2[k]
            if(set1[0]==set2[0]):
                item1=set1[0]
                item2=set1[1]
                item3=set2[1]
                newset=[item1,item2,item3]
                candidateSet3List[candidateListCount]=newset
                item1List=tBinaryFeatures[item1]
                item2List=tBinaryFeatures[item2]
                item3List=tBinaryFeatures[item3]
                totalList=item1List+item2List+item3List
                candidateSet3Count[candidateListCount]=Counter(totalList)[3]
                candidateListCount=candidateListCount+1
                noOfSelectedCandidateItems=noOfSelectedCandidateItems+1
            else : 
                break
    print "Total no of initial candidate items for set 3: ",noOfSelectedCandidateItems
    candidateSet3List,candidateSet3Count=evalCandidateSet3(frequentSet2,candidateSet3List,candidateSet3Count)
    print "Total no of final candidate items for set 3: ",len(candidateSet3List)," and no of pruned items : ",noOfSelectedCandidateItems-len(candidateSet3List)
    return candidateSet3List,candidateSet3Count
              
def getFrequentSet3(candidateSet3List,candidateSet3Count):
    frequentSet3=[]
    frequentSet3Count=[]
    noOfFrequentItems=0
    noOfInFrequentItems=0
    
    for i in range(0,len(candidateSet3List)):
        support=candidateSet3Count[i]/5000
        if support>=0.03:
            frequentSet3.append(candidateSet3List[i])
            frequentSet3Count.append(candidateSet3Count[i])
            noOfFrequentItems=noOfFrequentItems+1
        else:
            noOfInFrequentItems=noOfInFrequentItems+1
    
    print "Total Candidate Item sets at Stage 3: ",len(candidateSet3List)," No of Frequent Items selected : ",noOfFrequentItems," No of InFrequent Items pruned : ",noOfInFrequentItems
    return frequentSet3, frequentSet3Count

def ruleGenerationFrequencySet2(tBinaryFeatures,tFeatures,frequentSet2,frequentSet2Count):
    ruleListSet2=[]
    for i in range(0,len(frequentSet2)):
        support=frequentSet2Count[i]/5000
        itmAInd=frequentSet2[i][0]
        itmBInd=frequentSet2[i][1]
        
        countA=Counter(tBinaryFeatures[itmAInd])[1]
        countB=Counter(tBinaryFeatures[itmBInd])[1]
        
        rule1Confidance=frequentSet2Count[i]/countA
        rule2Confidance=frequentSet2Count[i]/countB
        if rule1Confidance>=0.25:
            itmAInd=frequentSet2[i][0]
            itmBInd=frequentSet2[i][1]
            itmA=tFeatures[itmAInd]
            itmB=tFeatures[itmBInd]
            ruleStr="if "+itmA+" Then "+itmB
            ruleItm=[ruleStr,rule1Confidance,support]
            ruleListSet2.append(ruleItm)
        if rule2Confidance>=0.25:
            itmAInd=frequentSet2[i][0]
            itmBInd=frequentSet2[i][1]
            itmA=tFeatures[itmAInd]
            itmB=tFeatures[itmBInd]
            ruleStr="if "+itmB+" Then "+itmA
            ruleItm=[ruleStr,rule2Confidance,support]
            ruleListSet2.append(ruleItm)
    return ruleListSet2
     
    
def ruleGenerationFrequencySet3(tBinaryFeatures,tFeatures,frequentSet3,frequentSet3Count):
    ruleListSet3=[]
    
    for i in range(0,len(frequentSet3)):
        support=frequentSet3Count[i]/5000
        itmAInd=frequentSet3[i][0]
        itmBInd=frequentSet3[i][1]
        itmCInd=frequentSet3[i][2]
        itmA=tFeatures[itmAInd]
        itmB=tFeatures[itmBInd]
        itmC=tFeatures[itmCInd]
        
        AB=tBinaryFeatures[itmAInd]+tBinaryFeatures[itmBInd]
        AC=tBinaryFeatures[itmAInd]+tBinaryFeatures[itmCInd]
        BC=tBinaryFeatures[itmBInd]+tBinaryFeatures[itmCInd]
        countAB=Counter(AB)[2]
        countAC=Counter(AC)[2]
        countBC=Counter(BC)[2]
        rule1Confidance=frequentSet3Count[i]/countAB
        rule2Confidance=frequentSet3Count[i]/countAC
        rule3Confidance=frequentSet3Count[i]/countBC
        
        if rule1Confidance>=0.25:
            ruleStr="if "+itmA+" and "+itmB+" Then "+itmC
            ruleItm=[ruleStr,rule1Confidance,support]
            ruleListSet3.append(ruleItm)
        if rule2Confidance>=0.25:
            ruleStr="if "+itmA+" and "+itmC+" Then "+itmB
            ruleItm=[ruleStr,rule2Confidance,support]
            ruleListSet3.append(ruleItm)
        if rule3Confidance>=0.25:
            ruleStr="if "+itmB+" and "+itmC+" Then "+itmA
            ruleItm=[ruleStr,rule2Confidance,support]
            ruleListSet3.append(ruleItm)
    
    return ruleListSet3 

def getTopRuleList(ruleList):
    ruleList.sort(key=lambda x: x[1],reverse=True)
    topRuleList=ruleList[:30]
    return topRuleList
                     
def main():
    # reading the data
    global dataTraining
    global reviewListTotal
    filename="stars_data.csv"
    dataTraining=readData.getData(filename)
    
    wordListTotal=[]
    classLabelP=[]
    classLabelN=[]
        
    # no of data
    noOfData=len(dataTraining)
    
    for i in range(0,noOfData):
        templist=WordList.getList(dataTraining[i][0])
        reviewListTotal.append(templist)
        wordListTotal.extend(templist)
        if(dataTraining[i][1]==1):
            classLabelP.append(1)
            classLabelN.append(0)
        else:
            classLabelP.append(0)
            classLabelN.append(1)   

    # get 2000 words ranked from 201 to 2200 in terms of frequency
    
    print "generating binary features"
    topWordList=TopWords.getList(wordListTotal)
    binaryFeatures=getBinaryFeatures(topWordList,classLabelP,classLabelN)
    tFeatures=topWordList
    tFeatures.append("isPositive")
    tFeatures.append("isNegative")
    tBinaryFeatures=np.array(binaryFeatures)
    tBinaryFeatures=tBinaryFeatures.transpose()
    
    joblib.dump(tBinaryFeatures,'tBinaryFeatures.pkl')
    joblib.dump(binaryFeatures,'binaryFeatures.pkl')
    joblib.dump(tFeatures,'tFeatures.pkl')
        
    
    print "Finished generating binary features"
    #get candidate set 1
    
    candidateSet1List,candidateSet1Count=getCandidateSet1(tBinaryFeatures)
    frequentSet1,frequentSet1Count= getFrequentSet1(candidateSet1List,candidateSet1Count)
    
    
    joblib.dump(frequentSet1,'frequentSet1.pkl')
    joblib.dump(frequentSet1Count,'frequentSet1Count.pkl')
    
    candidateSet2List,candidateSet2Count=getCandidateSet2(tBinaryFeatures,frequentSet1)
    frequentSet2,frequentSet2Count=getFrequentSet2(candidateSet2List,candidateSet2Count)
    
    joblib.dump(frequentSet2,'frequentSet2.pkl')
    joblib.dump(frequentSet2Count,'frequentSet2Count.pkl')
    
    candidateSet3List,candidateSet3Count=getCandidateSet3(tBinaryFeatures,frequentSet2)

    frequentSet3,frequentSet3Count=getFrequentSet3(candidateSet3List,candidateSet3Count)
    
    joblib.dump(frequentSet3,'frequentSet3.pkl')
    joblib.dump(frequentSet3Count,'frequentSet3Count.pkl')
    
    #generating rules    
    
    ruleListSet2=ruleGenerationFrequencySet2(tBinaryFeatures,tFeatures,frequentSet2,frequentSet2Count)
    ruleList=ruleListSet2
    ruleListSet3=ruleGenerationFrequencySet3(tBinaryFeatures,tFeatures,frequentSet3,frequentSet3Count)
    ruleList.extend(ruleListSet3)
    
    topRuleList=getTopRuleList(ruleList)
    for k in range(0,30):
        print topRuleList[k]
    
if __name__ == '__main__':
    main()
