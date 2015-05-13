from __future__ import division
import numpy as np
from collections import Counter
from sklearn.externals import joblib
import scipy.stats

def ruleGenerationFrequencySet2(tBinaryFeatures,tFeatures,frequentSet2,frequentSet2Count,bonferoni):

    ruleListSet2=[]
    threshold=0.05/bonferoni
    
    for i in range(0,len(frequentSet2)):
        support=frequentSet2Count[i]/5000
        itmAInd=frequentSet2[i][0]
        itmBInd=frequentSet2[i][1]
        
        countA=Counter(tBinaryFeatures[itmAInd])[1]
        countB=Counter(tBinaryFeatures[itmBInd])[1]
        countAB=Counter(tBinaryFeatures[itmAInd]+tBinaryFeatures[itmBInd])[2]
        
        I11=countAB
        I10=countA-countAB
        I01=countB-countAB
        I00=5000-(I11+I10+I01)
        
        contingencyTable=[[I11,I10],[I01,I00]]
        contingencyTable=np.array(contingencyTable)
        chisq,pValue,degreeOfFreedom,exp = scipy.stats.chi2_contingency(contingencyTable)
        
        rule1pValue=pValue
        rule2pValue=pValue
        
        if rule1pValue<=threshold:
            itmAInd=frequentSet2[i][0]
            itmBInd=frequentSet2[i][1]
            itmA=tFeatures[itmAInd]
            itmB=tFeatures[itmBInd]
            ruleStr="if "+itmA+" Then "+itmB
            ruleItm=[ruleStr,chisq,pValue,support]
            ruleListSet2.append(ruleItm)
        if rule2pValue<=threshold:
            itmAInd=frequentSet2[i][0]
            itmBInd=frequentSet2[i][1]
            itmA=tFeatures[itmAInd]
            itmB=tFeatures[itmBInd]
            ruleStr="if "+itmB+" Then "+itmA
            ruleItm=[ruleStr,chisq,pValue,support]
            ruleListSet2.append(ruleItm)
    return ruleListSet2

def getContigencyTable(tBinaryFeatures,itmAInd,itmBInd,itmCInd):
    xor=[1]*5000
    xor=np.array(xor)

    itmAList=tBinaryFeatures[itmAInd]
    itmBList=tBinaryFeatures[itmBInd]
    itmCList=tBinaryFeatures[itmCInd]        
    itmABarList=tBinaryFeatures[itmAInd]^xor
    itmBBarList=tBinaryFeatures[itmBInd]^xor
    itmCBarList=tBinaryFeatures[itmCInd]^xor        

    ABC=itmAList+itmBList+itmCList
    AbarBC=itmABarList+itmBList+itmCList
    ABbarC=itmAList+itmBBarList+itmCList
    AbarBbarC=itmABarList+itmBBarList+itmCList
    
    ABCbar=itmAList+itmBList+itmCBarList
    AbarBCbar=itmABarList+itmBList+itmCBarList
    ABbarCbar=itmAList+itmBBarList+itmCBarList
    AbarBbarCbar=itmABarList+itmBBarList+itmCBarList
            
    I11=Counter(ABC)[3]
    I10=Counter(ABCbar)[3]
    I01=Counter(AbarBC)[3]+Counter(ABbarC)[3]+Counter(AbarBbarC)[3]
    I00=Counter(AbarBCbar)[3]+Counter(ABbarCbar)[3]+Counter(AbarBbarCbar)[3]
    
    contingencyTable=[[I11,I10],[I01,I00]]
    contingencyTable=np.array(contingencyTable)

    return contingencyTable 
    
def ruleGenerationFrequencySet3(tBinaryFeatures,tFeatures,frequentSet3,frequentSet3Count,bonferoni):
    ruleListSet3=[]
    threshold=0.05/bonferoni
    
    for i in range(0,len(frequentSet3)):
        support=frequentSet3Count[i]/5000
        itmAInd=frequentSet3[i][0]
        itmBInd=frequentSet3[i][1]
        itmCInd=frequentSet3[i][2]
        
        itmA=tFeatures[itmAInd]
        itmB=tFeatures[itmBInd]
        itmC=tFeatures[itmCInd]
        
        
        rule1ContingencyTable=getContigencyTable(tBinaryFeatures,itmAInd,itmBInd,itmCInd)
        rule2ContingencyTable=getContigencyTable(tBinaryFeatures,itmAInd,itmCInd,itmBInd)
        rule3ContingencyTable=getContigencyTable(tBinaryFeatures,itmCInd,itmBInd,itmAInd)
        
        
        chisq1,pValue1,degreeOfFreedom1,exp1 = scipy.stats.chi2_contingency(rule1ContingencyTable)
        chisq2,pValue2,degreeOfFreedom2,exp2 = scipy.stats.chi2_contingency(rule2ContingencyTable)
        chisq3,pValue3,degreeOfFreedom3,exp3 = scipy.stats.chi2_contingency(rule3ContingencyTable)
        
        
        if pValue1<=threshold:
            ruleStr="if "+itmA+" and "+itmB+" Then "+itmC
            ruleItm=[ruleStr,chisq1,pValue1,support]
            ruleListSet3.append(ruleItm)
        if pValue1<=threshold:
            ruleStr="if "+itmA+" and "+itmC+" Then "+itmB
            ruleItm=[ruleStr,chisq2,pValue2,support]
            ruleListSet3.append(ruleItm)
        if pValue1<=threshold:
            ruleStr="if "+itmB+" and "+itmC+" Then "+itmA
            ruleItm=[ruleStr,chisq3,pValue3,support]
            ruleListSet3.append(ruleItm)
    
    return ruleListSet3 

def getTopRuleList(ruleList):
    ruleList.sort(key=lambda x: x[1],reverse=True)
    topRuleList=ruleList[:30]
    return topRuleList
                     
def main():
    
    tBinaryFeatures=joblib.load('tBinaryFeatures.pkl')
    tFeatures=joblib.load('tFeatures.pkl')
    
    frequentSet2=joblib.load('frequentSet2.pkl')
    frequentSet2Count=joblib.load('frequentSet2Count.pkl')
    
    frequentSet3=joblib.load('frequentSet3.pkl')
    frequentSet3Count=joblib.load('frequentSet3Count.pkl')
    
    bonferoni=(2*len(frequentSet2))+(3*len(frequentSet3))
    ruleListSet2=ruleGenerationFrequencySet2(tBinaryFeatures,tFeatures,frequentSet2,frequentSet2Count,bonferoni)
    ruleList=ruleListSet2
    ruleListSet3=ruleGenerationFrequencySet3(tBinaryFeatures,tFeatures,frequentSet3,frequentSet3Count,bonferoni)
    ruleList.extend(ruleListSet3)
    
    
    
    topRuleList=getTopRuleList(ruleList)
    for k in range(0,30):
        print topRuleList[k]

    
if __name__ == '__main__':
    main()
