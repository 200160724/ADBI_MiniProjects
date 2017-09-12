import pandas as pd
import numpy as np
import igraph
from random import shuffle
import sys
from scipy import spatial

def main():
    attribute_vectors=pd.read_csv('C:\\Users\\abhis\\Documents\\fb_caltech_small_attrlist.csv').values
    g = igraph.Graph.Read_Ncol('C:\\Users\\abhis\\Documents\\fb_caltech_small_edgelist.txt')
    membershipList=range(324)
    alpha=1
    for iteration in range(15) :
        print(iteration)
        stillworking=-1
        for i in range(324):
            maximumDelta=0
            bestMaskList=membershipList
            initialStructMod=g.modularity(membershipList)
            for j in range(324):
                if (membershipList[i]!=membershipList[j]):
                    totalDelta=0                  
                    tempMaskList=list(membershipList)
                    tempMaskList[i]=membershipList[j]
                    finalStructMod=g.modularity(tempMaskList)
                    deltaAttrMod=attr_modularity_cluster(membershipList,membershipList[j],i,attribute_vectors)
                    deltaStructMod=finalStructMod-initialStructMod
                    totalDelta=alpha*(deltaStructMod) + (1-alpha)*(deltaAttrMod)
                    if ((totalDelta>maximumDelta) & ((deltaStructMod)>0)):
                        stillworking=1
                        maximumDelta=totalDelta
                        bestMaskList=tempMaskList       
            membershipList=bestMaskList

        if stillworking==-1:
            break

        print(membershipList)
        clusterlist=list(set(membershipList))
        
        newcluster={}
        for c in clusterlist:
            newcluster[c]=c

        masterList=list(membershipList)  
        for i in clusterlist:
            maximumDelta=0
            bestMaskList=membershipList
            bestj=-1
            initialStructMod=g.modularity(membershipList)
            for j in clusterlist:
                if (newcluster[i]!=newcluster[j]):
                    totalDelta=0
                    tempMaskList=list(membershipList)
                    for idx, item in enumerate(masterList):
                        if item == i:
                            tempMaskList[idx] = newcluster[j]
                            
                    finalStructMod=g.modularity(tempMaskList)
                    deltaAttrMod=0
                    length=0
                    for idx, item in enumerate(masterList):                    
                        if item == i:                        
                            deltaAttrMod=deltaAttrMod+attr_modularity_cluster(membershipList,newcluster[j],idx,attribute_vectors)
                            length=length+1
                    deltaAttrMod=deltaAttrMod/length
                    deltaStructMod=finalStructMod-initialStructMod
                    totalDelta=alpha*(deltaStructMod) + (1-alpha)*(deltaAttrMod)
                    if ((totalDelta>maximumDelta) & (deltaStructMod>0)):
                        b1=finalStructMod-initialStructMod
                        b2=deltaAttrMod
                        maximumDelta=totalDelta
                        bestMaskList=tempMaskList
                        bestj=j
            if bestj!=-1:
                newcluster[i]=newcluster[bestj]
                membershipList=bestMaskList
        print(membershipList)

    if alpha==0:
        f = open('communities_0.txt','w')
    elif alpha==0.5:
        f = open('communities_5.txt','w')
    elif alpha==1:
        f = open('communities_1.txt','w')
    
    clusters=list(set(membershipList))
    for cluster in clusters:
        indices = [k for k, x in enumerate(membershipList) if x == cluster]
        print >>f,(", ".join(str(s) for s in indices))
        
    

def attr_modularity_cluster(membership,cluster,newentrant,attr_vectors):
    cs=0
    indices = [k for k, x in enumerate(membership) if x == cluster]
    for i in indices:
        cs=cs+(1-spatial.distance.cosine(attr_vectors[i], attr_vectors[newentrant]))
    return cs/len(indices)
    
            
         
if __name__ == "__main__":
    main()
