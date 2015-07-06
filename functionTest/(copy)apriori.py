#-*- coding:utf-8 -*-
def loadDataSet():  
    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]  
    #return [[c++, java, python], [php, java, 网页], [c++, php,java, 网页], [php, 网页]]  
    return [['c','java','python'], ['php','c#','网页'], ['c','php','java','网页'], ['php','网页']]  
def LoadData( FileName,Charactor = ','):
    fin = open(FileName,'r')
    #TempTrans = [[TypeChange(x.split(Charactor)) ] for x in fin]
    TempTrans = []
    for x in fin:
        TempList = []
        ItemList = x.split(Charactor)
        for il in ItemList:
            #print 'il=',il
            #if cmp(il,'\n')==0:
            #    print 'n'
            if il.endswith('\n'): #match end
                #TempList.append(il.replace('\n', ''))
            #    print 'nnnn'
                pass
            else:
                TempList.append(il)
        TempTrans.append(TempList)
    fin.close()
    return TempTrans
#def TypeChange(ItemList):
#    TempList = []
#    for x in ItemList:
#        print 'x=',x
#        if cmp(x,'\n')==0:
#            print 'nn'
#        if x.endswith('\n'): #match end
#            TempList.append(x.replace('\n', ''))
#        else:
#            TempList.append(x)
#    return TempList
   
def createC1(dataSet):# return C1 frequent item set  
    C1 = []  
    for transaction in dataSet:  
        for item in transaction:  
            if not [item] in C1:  
                C1.append([item])  
    C1.sort()  
    return map(frozenset,C1) # frozenset can't changed !  
  
def scanD(D,CK,minSupport):  
    ssCnt = {}  
    for tid in D:  
        for can in CK:  
            if can.issubset(tid):  
                if not ssCnt.has_key(can): ssCnt[can]=1  
                else:ssCnt[can]+=1  
    numItems = float(len(D))  
    retList = []  
    supportData = {}  
    for key in ssCnt:  
        support = ssCnt[key]/numItems  
        if support >= minSupport:  
            retList.insert(0, key)  
        supportData[key]= support  
          
    return retList,supportData # return result list and support data is a map  
  
def aprioriGen(Lk,k):  
    retList = []  
    lenLk = len(Lk)  
    for i in range(lenLk):  
        for j in range(i+1,lenLk):  
            L1 = list(Lk[i])[:k-2] ;  L2 = list(Lk[j])[:k-2]  
            L1.sort();L2.sort()  
            if L1 == L2:  
                retList.append(Lk[i]| Lk[j])  
    return retList  
  
def apriori(dataSet,minSupport = 0.5):  
    C1 = createC1(dataSet)  
    D = map(set, dataSet)  
    L1,supportData = scanD(D, C1, minSupport)  
    L = [L1]  
    k = 2  
    while(len(L[k-2])>0):  
        Ck = aprioriGen(L[k-2], k)  
        Lk,supK = scanD(D, Ck, minSupport)  
        supportData.update(supK)  
        L.append(Lk)  
        k+=1  
    return L,supportData  
def generateRules(L,supportData2,minConf = 0.7): 
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i>1):    #即只有一项而已
                rulesFromConseq(freqSet,H1,supportData2,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData2,bigRuleList,minConf)
    return bigRuleList

def calcConf(freqSet,H,supportData,br1,minConf = 0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf>= minConf:
            print freqSet-conseq[0],' --> ',conseq,'support=',supportData[freqSet], 'confidence=',conf
            #br1.append((freqSet-conseq,conseq,supportData(freqSet],conf))
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet,H,supportData,br1,minConf = 0.7):
    m = len(H[0])
    if (len(freqSet)>(m+1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if (len(Hmp1)>1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)
      
if __name__ == "__main__":  
    #dataSet = LoadData('./data.txt') 
    dataSet = loadDataSet() 
    #print 'dataSet=',dataSet
    for ds in dataSet:
        for dl in ds:
            print dl,
        print ''
    #print '----------------------------'
    #print '----------------------------'
    #singleData = createC1(dataSet) 
    #print 'singleData',singleData
    #print '----------------------------'
    #print '----------------------------'
    #dataSetFrozenset  = map(set, dataSet) 
    #print 'dataSetFrozenset=',dataSetFrozenset  
    #print '----------------------------'
    #print '----------------------------'
    #L1,supportData = scanD(dataSetFrozenset,singleData , 0.5)   #supportData 是每一项出现的频率
    #print 'L1=',L1 
    #print '----------------------------'
    #print '----------------------------'
    #print 'supportData=',supportData 
    #dataSet = loadDataSet()  
    L,supportData2 = apriori(dataSet)  
    print '----------------------------'
    print '----------------------------'
    #print 'supportData2=',supportData2       #supportData2  是多项出现的频率
    rules = generateRules(L,supportData2,0.5)
    print rules
