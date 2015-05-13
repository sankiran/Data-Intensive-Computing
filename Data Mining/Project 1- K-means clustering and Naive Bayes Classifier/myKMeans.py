from sklearn.cluster import KMeans
def getModel(dataMatrix,noOfClusters):
    learn=KMeans(n_clusters=noOfClusters,tol=0.0001)
    learn.fit(dataMatrix)
    return learn

def getClusterData(labels,wordList,noOfClusters):
    clusterData = [[] for _ in xrange(noOfClusters)]
    for i in range(0,len(labels)):
        clusterData[labels[i]].append(wordList[i])
    return clusterData
