# !/usr/bin/env python
# -*- coding:utf-8 -*-
import workManagerForApriori
class save_apriori_result_to_database():
    def __init__(self,workNum = 200,threadNum= 5):
    #jobhref_spider = spider.jobSpider()

    #countThread = 1   # count the number Thread
    #countPage = 1     #cout the number of page
    #myHref = 0   # judge 'myHref' is none or not
    #countJob= 1
    #countAddJob = 2
        self.myThreadPool = ''
        self.workNum = workNum
        self.threadNum = threadNum

    def save_apriori_data(self,apriori_result = []):
        self.myThreadPool = workManagerForApriori.WorkManager(self.threadNum,self.threadNum)
        self.myThreadPool.my__init_thread_pool()
        count = 0
        for result in apriori_result:
            count = count + 1
            self.myThreadPool.my__init_work_queue(result[0],result[1],result[2],result[3],count)
            print 'count =',count
        while self.myThreadPool.check_queue() != 0 :
            self.myThreadPool.wait_allcomplete() 
            print 'test'


	#print type(myThreadPool.check_queue())
        #while myThreadPool.check_queue() >=0 and myThreadPool.check_queue() <= 100:
        #    print 'myThreadPool.check_queue() ' , myThreadPool.check_queue() 
        #    print '\n\n\n\n'
	#    countAddJob += 1
	#    print 'countJob = ' , countJob
        #    myHref = 0
	#    while myHref == 0: 
	#        myHref = jobhref_spider.get_first_jobhref(countPage)
	#	if myHref != 0:
	#	    print 'countPage = ' ,countPage
	#	    print '\n\n\n\n\n'
	#    countPage += 1	
        #    for href in myHref:     #把url加入到任务队列中
        #        myThreadPool.my__init_work_queue(href,countJob)
	#        countJob += 1
        #    countThread += 1

