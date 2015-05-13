from sklearn.externals import joblib
def getList(wordlist):
    myWordList=[]
    dictionary={}
    i=1
    for word in wordlist:
        if(dictionary.has_key(word)):
            dictionary[word]+=1
        else :
            dictionary[word]=1
    for word in sorted(dictionary, key=dictionary.get, reverse=True):
        if(i>100 and i<=2100):
            myWordList.append(word)
        i=i+1
    joblib.dump(myWordList,'myWordList.pkl')
    return myWordList
