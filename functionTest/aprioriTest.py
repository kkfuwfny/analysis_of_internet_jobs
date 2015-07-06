#-*-coding:utf-8 -*-
import apriori
import time
print 'start...'
startTime = time.clock()
#dataSet=apriori.loadDataSet()
#dataSet = apriori.LoadData('./data3.txt')
dataSet = apriori.LoadData('./data.txt')
#print 'dataSet=',dataSet
C1=apriori.createC1(dataSet)

D=map(set,dataSet)
L1,suppData0=apriori.scanD(D,C1,0.5)

L,suppData=apriori.apriori(dataSet)

print 'type(L)=',type(L)
print 'L=',L

#rules=apriori.generateRules(L,suppData,minConf=0.5)

endTime = time.clock()
print "runing time is :%.03f second" % (endTime - startTime)
