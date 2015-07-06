# !/usr/bin/env python
# -*- coding:utf-8 -*-
# ref_blog:http://www.open-open.com/home/space-5679-do-blog-id-3247.html

import Queue
import threading
import time
import spider
import random
from bloomFilter import bloomfilter  #judge the job is saved or not

mutex = threading.RLock() #the thread lock be used synchronization
bFilter = bloomfilter.BloomFilter('./bloomFilter/jobHash.txt')
class WorkManager(object):
    def __init__(self, work_num=20,thread_num=5):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.work_num = work_num
        self.thread_num = thread_num
        #self.__init_work_queue(work_num)
        #self.__init_thread_pool(thread_num)

    """
        初始化线程
    """
    def my__init_thread_pool(self):
    #def __init_thread_pool(self):
        for i in range(self.thread_num):
            self.threads.append(Work(self.work_queue))
	return "test return workManager.py + '\n\n\n\n\n\n'"

    """
        初始化工作队列
    """
    #def __init_work_queue(self, href = 'test'):
    def my__init_work_queue(self, href = 'testUrl',countJob = 1):
        #for i in range(jobs_num):
        self.add_job(self.do_job, href,countJob)
	
    """
        添加一项工作入队
    """
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))#任务入队，Queue内部实现了同步机制
    """
        检查剩余队列任务
    """
    def check_queue(self):
        return self.work_queue.qsize()

    """
        等待所有线程运行完毕
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

    def do_job(self,args):
        print 'function do_job() start...'
        time.sleep(random.randint(3,10))#模拟处理时间
        print "countJob(args[1]) = " , args[1]        
        mainSpider = spider.jobSpider()
        href = args[0]
	if bFilter.isContaions(href) == False:
            if mainSpider.get_jobs(href) == 1:     #获取信息成功
                bFilter.insert(href)   #做标记，已经存了
                mutex.acquire()      #lock.in order to synchronization 
		print '开始存储岗位基本信息'                
		mainSpider.save_data()
		print '开始存储课程集合和地点'
		mainSpider.save_job_course_set_and_workplace()
                mutex.release()      #unlock
	else:
            print '%s the job has exists' % href
        print threading.current_thread(), list(args)
	
	#测试返回的数据在哪里
	#return "test return workManager.py + '\n\n\n\n\n\n'"
class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                #do, args = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do, args = self.work_queue.get(timeout = 20)#任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done()#通知系统任务完成
            except Exception,e:
                print str(e)
                #break
                continue
#具体要做的任务
"""
if __name__ == '__main__':
    start = time.time()
    work_manager =  WorkManager(10, 2)#或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()
    end = time.time()
    print "cost all time: %s" % (end-start)
"""
