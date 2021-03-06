#-*- coding:utf-8 -*-
import time
import re
def loadDataSet():  
    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]  
    #return [[c++, java, python], [php, java, 网页], [c++, php,java, 网页], [php, 网页]]  
    return [['c','java','python'], ['php','c#','网页'], ['c','php','java','网页'], ['php','网页'],['c','yy','java']]  
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
                TempList.append(il.strip('\n'))
                pass
            else:
                TempList.append(il)
        TempTrans.append(TempList)
    fin.close()
    return TempTrans
   
def createC1(dataSet):# return C1 frequent item set  
    C1 = []  
    for transaction in dataSet:  
        for item in transaction:  
            if not [item] in C1:  
                C1.append([item])  
    C1.sort()  
    return map(frozenset,C1) # frozenset can't changed !  
    #return map(list,C1)
  
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
    #print 'D=',D
    L1,supportData = scanD(D, C1, minSupport)  
    #print 'L1=',L1
    #for l in L1:
    #    for x in l:
    #        print 'x=',x
    L = [L1]  
    #print 'LL=',L
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
        if supportData.get(freqSet) is not None and supportData.get(freqSet-conseq) is not None: 
            #print 'supportData[freqSet]=',supportData[freqSet]
            #print 'supportData[freqSet-conseq]=',supportData[freqSet-conseq]
            conf = supportData[freqSet]/supportData[freqSet-conseq]
            if conf>= minConf:
                fc_set = ''
                con_set = ''
                for fc in freqSet-conseq:
                    fc_set = fc_set + ',' + fc 
                r = re.compile(',')
                fc_set = r.sub('',fc_set,1)
                print fc_set,'-->',
                for con in conseq:
                    con_set = con_set + ',' + con
                r = re.compile(',')
                con_set = r.sub('',con_set,1)
                print con_set,
                print 'support=',supportData[freqSet],'confidence=',conf
                #print freqSet-conseq,' --> ',conseq,'support=',supportData[freqSet], 'confidence=',conf
                #br1.append((freqSet-conseq,conseq,supportData(freqSet,conf))
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


def analysis_popular_workplace():
    dataSet = LoadData('./testWorkplace.txt')
    singleData = createC1(dataSet) 
    dataSetFrozenset  = map(set, dataSet) 
    L1,supportData = scanD(dataSetFrozenset,singleData , 0)   #supportData 是每一项出现的频率
    workplace = []    ## 工作地点列表
    for key , value in supportData.iteritems():
        wp = ''
        for k in key:
        #    print k,
            wp = k
        #print ':',value*42127
        workplace.append((wp,value*42127))

    workplace.sort(key=lambda x:x[1],reverse = True)
    for wp in workplace:
        for w in wp:
            print w
    return workplace


def analysis_popular_course():
    dataSet = LoadData('./tx.txt')
    singleData = createC1(dataSet) 
    dataSetFrozenset  = map(set, dataSet) 
    L1,supportData = scanD(dataSetFrozenset,singleData , 0)   #supportData 是每一项出现的频率
    #print 'dataSetFrozenset=',dataSetFrozenset  
    pop_course = []    ## 工作地点列表
    for key , value in supportData.iteritems():
        wp = ''
        for k in key:
        #    print k,
            wp = k
        #print ':',value*42127
        pop_course.append((wp,value*4114))

    pop_course.sort(key=lambda x:x[1],reverse = False)
    for wp in pop_course:
        for w in wp:
            print w
    return pop_course

if __name__ == "__main__":  
    
    
    #dataSet = LoadData('./data.txt') 
    #dataSet = LoadData('./tx.txt') 
   
    #dataSet = loadDataSet() 
    
    
    #print 'dataSet=',dataSet
    #print '----------------------------'
    #print '----------原始数据----------'
    #print '----------------------------'
    #for ds in dataSet:
    #    for dl in ds:
    #        print dl,
    #    print ''


    '''
    print '----------------------------'
    print '----------------------------'
    singleData = createC1(dataSet) 
    dataSetFrozenset  = map(set, dataSet) 
    #print '----------------------------'
    #print '----------------------------'
    L1,supportData = scanD(dataSetFrozenset,singleData , 0)   #supportData 是每一项出现的频率
    print '-------supportDat-----------'
    print '--------各项频率------------'
    print '----------------------------'
    '''
#############################################
    
    ## 工作地点列表
    #workplace = analysis_popular_workplace()
    workplace = analysis_popular_course()
    
    #sortedData=sorted(supportData.items(), key=lambda x:x[1],reverse=False)  #reverse=True 为降序，反为升序 
    #sortedData = list(sortedData) 
    for wp in workplace:
        for w in wp:
            print w
    
    #startTime = time.clock()
    #print '-------supportData2---------'
    #print '--------各项频率------------'
    #print '----------------------------'
    #freqSet,supportData2 = apriori(dataSet,0.05)  
###############################################

    #ls_set = []
    #for key , value in supportData2.iteritems():
    #    k_set = ''
    #    for k in key:
    #        k_set = k_set + k + ','
    #        print k,
    #    print ':',value*4223
    #    ls_set.append((k_set,value*4223))
    #    ls_set.sort(key=lambda x:x[1])
    #for l in ls_set:
    #    print l[0],':',l[1]
    #sortedData=sorted(supportData2.items(), key=lambda x:x[1],reverse=False)  #reverse=True 为降序，反为升序 
    #for sd in sortedData:
    #    print sd
    print '----------------------------'
    print '---------关联分析-----------'
    #sortedData=sorted(supportData.items(), key=lambda x:x[1],reverse=False)  #reverse=True 为降序，反为升序 

    ############################
    #rules = generateRules(freqSet,supportData2,0)
    ##print type(rules)
    #endTime = time.clock()
    #print "runing time is :%.03f second" % (endTime - startTime) 
############################################
