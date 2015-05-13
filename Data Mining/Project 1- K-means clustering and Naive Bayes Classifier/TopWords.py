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
        if(i>200 and i<=2200):
            myWordList.append(word)
        i=i+1
    return myWordList
