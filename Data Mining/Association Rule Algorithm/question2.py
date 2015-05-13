from __future__ import division
import numpy as np
from collections import Counter
from sklearn.externals import joblib
import scipy.stats

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
    
    tBinaryFeatures=joblib.load('tBinaryFeatures.pkl')
    tFeatures=joblib.load('tFeatures.pkl')
    
    frequentSet2=joblib.load('frequentSet2.pkl')
    frequentSet2Count=joblib.load('frequentSet2Count.pkl')
    
    frequentSet3=joblib.load('frequentSet3.pkl')
    frequentSet3Count=joblib.load('frequentSet3Count.pkl')
    
    antecedent1="worst"
    consequent1="isNegetive"
    
    indexAntecendent1=tFeatures.index(antecedent1)
    indexConsequent1=tFeatures.index(consequent1)
    
    AB=Counter(tBinaryFeatures[indexAntecendent1]+tBinaryFeatures[indexConsequent1])[2]
    A=Counter(tBinaryFeatures[indexAntecendent1])[1]
    B=Counter(tBinaryFeatures[indexConsequent1])[1]
    
    I11=AB
    I10=A-AB
    I01=B-AB
    I00=5000-(I11+I10+I01)
    
    contingencyTable=[[I11,I10],[I01,I00]]
    contingencyTable=np.array(contingencyTable)
    print "Rule: ",antecedent1," -> ",consequent1
    print contingencyTable
    
    chisq,pValue,degreeOfFreedom,exp = scipy.stats.chi2_contingency(contingencyTable)
    
    print chisq,pValue,degreeOfFreedom,exp
    
    
if __name__ == '__main__':
    main()
