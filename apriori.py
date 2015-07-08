#-*- coding:utf-8 -*-
import time
import re
import jobDB
import MySQLdb
import saveAprioriResultToDataBaseThreadPool
apr_db = jobDB.jobDB()
class apriori():

    def __init__(self):
        self.fre_set = []      #这个是频繁项的集合
        self.apriori_course_result_list = []  #这个列表是用于保存那个关联分析结果的
        self.count_apriori_coure = 0
        self.position_count = 0   #这个数字会返回去，然后显示在分析数据的面板上，就是统计相应分析的岗位总数
        #self.merge_fc_con = []
        try:
            self.conn = MySQLdb.connect (user='root',passwd='3288',host='127.0.0.1', port=3306,charset='utf8')
            self.cur = self.conn.cursor()
            self.conn.select_db('51job')
        except MySQLdb.Error,e:
            print "MySQLdb Error %d: %s" % (e.args[0], e.args[1])

    def loadDataSet(self):  
        #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]  
        #return [[c++, java, python], [php, java, 网页], [c++, php,java, 网页], [php, 网页]]  
        return [['c','java','python'], ['php','c#','网页'], ['c','php','java','网页'], ['php','网页'],['c','yy','java']]  

    def LoadData(self, FileName,Charactor = ','):
        fin = open(FileName,'r')
        #TempTrans = [[TypeChange(x.split(Charactor)) ] for x in fin]
        TempTrans = []
        for x in fin:
            self.position_count = self.position_count + 1
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
       
    def createC1(self,dataSet):# return C1 frequent item set  
        C1 = []  
        for transaction in dataSet:  
            for item in transaction:  
                if not [item] in C1:  
                    C1.append([item])  
        C1.sort()  
        return map(frozenset,C1) # frozenset can't changed !  
        #return map(list,C1)
    
    #这个函数是返回单项出现的频率  
    def scanD(self,D,CK,minSupport):  
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
      
    def aprioriGen(self,Lk,k):  
        retList = []  
        lenLk = len(Lk)  
        for i in range(lenLk):  
            for j in range(i+1,lenLk):  
                L1 = list(Lk[i])[:k-2] ;  L2 = list(Lk[j])[:k-2]  
                L1.sort();L2.sort()  
                if L1 == L2:  
                    retList.append(Lk[i]| Lk[j])  
        return retList  
     
 
    #返回频繁项
    def apriori(self,dataSet,minSupport = 0.5):  
        C1 = self.createC1(dataSet)  
        D =map(set, dataSet)  
        #print 'D=',D
        L1,supportData = self.scanD(D, C1, minSupport)  
        #print 'L1=',L1
        #for l in L1:
        #    for x in l:
        #        print 'x=',x
        L = [L1]  
        #print 'LL=',L
        k = 2  
        while(len(L[k-2])>0):  
            Ck = self.aprioriGen(L[k-2], k)  
            Lk,supK = self.scanD(D, Ck, minSupport)  
            supportData.update(supK)  
            L.append(Lk)  
            k+=1  
        return L,supportData 

    def generateRules(self,L,supportData2,minConf = 0.7): 
        bigRuleList = []
        for i in range(1,len(L)):
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                if (i>1):    #即不只有一项而已
                    self.rulesFromConseq(freqSet,H1,supportData2,bigRuleList,minConf)
                else:
                    self.calcConf(freqSet,H1,supportData2,bigRuleList,minConf)
        return bigRuleList

    #关联分析的主要函数， 输出 X-->Y
    def calcConf(self,freqSet,H,supportData,br1,minConf = 0.7):
        #print 'function apriori.calcConf() starting'
        prunedH = []
        for conseq in H:
            if supportData.get(freqSet) is not None and supportData.get(freqSet-conseq) is not None: 
                #print 'supportData[freqSet]=',supportData[freqSet]
                #print 'supportData[freqSet-conseq]=',supportData[freqSet-conseq]
                conf = supportData[freqSet]/supportData[freqSet-conseq]
                if conf>= minConf:
                    self.count_apriori_coure = self.count_apriori_coure + 1
                    fc_set = ''
                    con_set = ''
                    merge_fc_con = ''
                    for fc in freqSet-conseq:
                        fc_set = fc_set + ',' + fc 
                    r = re.compile(',')
                    fc_set = r.sub('',fc_set,1)
                    #print fc_set,'-->',
                    for con in conseq:
                        con_set = con_set + ',' + con
                    r = re.compile(',')
                    con_set = r.sub('',con_set,1)
                    #print con_set,
                    merge_fc_con = fc_set + '-->' + con_set
                    #self.apriori_course_result_list.append((supportData[freqSet],conf,fc_set,con_set))
                    #存入数据库中
                    support = "%.4f" % supportData[freqSet]
                    support = str(support)
                    confidence = "%.4f" % conf
                    confidence = str(confidence)

                    self.apriori_course_result_list.append((support,confidence,fc_set,con_set))

                    #self.save_data(support,confidence,fc_set,con_set)
		    #apr_db.save_to_apriori_all_result(support,confidence,fc_set,con_set)


                    #print 'support=',supportData[freqSet],'confidence=',conf
                    #print 'count_apriori_coure =',self.count_apriori_coure
                    #print freqSet-conseq,' --> ',conseq,'support=',supportData[freqSet], 'confidence=',conf
                    #br1.append((freqSet-conseq,conseq,supportData(freqSet,conf))
                    br1.append((freqSet-conseq,conseq,conf))
                    prunedH.append(conseq)
        #print 'function apriori.calcConf() ended!'
        return prunedH

    def rulesFromConseq(self,freqSet,H,supportData,br1,minConf = 0.7):
        m = len(H[0])
        if (len(freqSet)>(m+1)):
            Hmp1 = self.aprioriGen(H, m+1)
            Hmp1 = self.calcConf(freqSet, Hmp1, supportData, br1, minConf)
            if (len(Hmp1)>1):
                self.rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)


    #工作地点热度的分析
    def analysis_popular_workplace(self,filename = 'a'):
        self.position_count = 0 # 先清零，把上次的分析的统计数量去除掉
        print 'function apriori.analysis_popular_workplace() staring'
        #dataSet = self.LoadData('./testWorkplace.txt')
        dataSet = self.LoadData(filename)
        singleData = self.createC1(dataSet) 
        dataSetFrozenset  =map(set, dataSet) 
        L1,supportData = self.scanD(dataSetFrozenset,singleData , 0)   #supportData 是每一项出现的频率
        workplace = []    ## 工作地点列表
        for key , value in supportData.iteritems():
            wp = ''
            for k in key:
            #    print k,
                wp = k
            #print ':',value*42127
            workplace.append((wp,value))
        workplace.sort(key=lambda x:x[1],reverse = True)
        #for wp in workplace:
        #    for w in wp:
                #print w
        return workplace,self.position_count

    #热门课程的分析
    def analysis_popular_course(self,filename = 'a'):
        self.position_count = 0 # 先清零，把上次的分析的统计数量去除掉
        #dataSet = self.LoadData('./tx.txt')
        dataSet = self.LoadData(filename)
        singleData = self.createC1(dataSet) 
        dataSetFrozenset  = map(set, dataSet) 
        L1,supportData = self.scanD(dataSetFrozenset,singleData , 0)   #supportData 是每一项出现的频率
        #print 'dataSetFrozenset=',dataSetFrozenset  
        pop_course = []    ## 工作地点列表
        for key , value in supportData.iteritems():
            wp = ''
            for k in key:
            #    print k,
                wp = k
            #print ':',value*42127
            pop_course.append((wp,value))

        pop_course.sort(key=lambda x:x[1],reverse = True)
        #for wp in pop_course:
        #    for w in wp:
                #print w
        return pop_course,self.position_count

    #课程关联分析 
    def apriori_course(self,fileName = '',support = 0.05, confidence = 0.005):
	my_support = support
	my_confidence = confidence
        self.position_count = 0 # 先清零，把上次的分析的统计数量去除掉
        #dataSet = self.LoadData('./tx.txt') 
        #dataSet = self.loadDataSet()  #内置的数据，用来做测试而已
        dataSet = self.LoadData(fileName) 
        #print 'fileName =',fileName
        self.apriori_course_result_list = [] #清空数据，防止再次搜索时，上次的数据会在里面
        singleData = self.createC1(dataSet) 
        dataSetFrozenset  = map(set, dataSet) 
        L1,supportData = self.scanD(dataSetFrozenset,singleData , 0)   #supportData 是每一项出现的频率
        #startTime = time.clock()
        
	freqSet,supportData2 = self.apriori(dataSet,my_support)  

        ###############################################
        '''
        #频繁项集合
        self.fre_set = []
        for key , value in supportData2.iteritems():
            k_set = ''
            for k in key:
                k_set = k_set + k + ','
                #print k,
            #print ':',value*4223
            self.fre_set.append((k_set,value*4223))
            self.fre_set.sort(key=lambda x:x[1])  #对self.fre_set集合排序
        #for l in self.fre_set:
        #    print 'l[0]=',l[0],':',l[1]
        '''
        #print 'startTime =',startTime
        rules = self.generateRules(freqSet,supportData2,my_confidence)
        #s_data = saveAprioriResultToDataBaseThreadPool.save_apriori_result_to_database(self.count_apriori_coure,60)
        return self.apriori_course_result_list ,self.position_count

    #不出意外这个函数以后会用不到，因为不会保存分析的结果，所以故此提醒后来的维护人员
    def save_data(self,support,confidence,apriori_x,apriori_y):
        print "function save_data()..."
        sql = "insert into apriori_all_result(support,confidence,apriori_x,apriori_y) values (%s,%s,%s,%s)"
        info = (support,confidence,apriori_x,apriori_y)
        self.cur.execute(sql,info)
        self.conn.commit()
        print "function save_data() ended!"
    
        

    
    #def __del__(self):
    #    self.cur.close()
    #    self.conn.close()
            
if __name__ == "__main__":  
    apr = apriori()    
    apr.apriori_course()    


