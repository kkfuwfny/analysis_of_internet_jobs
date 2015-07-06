# !/usr/bin/env python
# -*- coding:utf-8 -*-

import newThread

if __name__ == '__main__':
    countThread = 1
    myThreadPool = newThread.WorkManager(20,2)
    for i in range(20):
        print 'i = ',i
        myThreadPool.my__init_work_queue(str(countThread))
	countThread += 1
    print 'start'
    myThreadPool.my__init_thread_pool()
    print 'end'
    print '\n\n\n' + 'test' 
    while True:
	#print type(myThreadPool.check_queue())
        if myThreadPool.check_queue() >=6 and myThreadPool.check_queue() <= 10:
	    print 'myThreadPool.check_queue() = ' , myThreadPool.check_queue()
            while myThreadPool.check_queue() != 50:
                myThreadPool.my__init_work_queue(str(countThread))
		countThread += 1





