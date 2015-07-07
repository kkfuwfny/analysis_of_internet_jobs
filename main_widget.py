# -*- coding: utf-8 -*-

"""
Module implementing main_widget.
"""
#修改系统的默认编码,不然那个listWidget显示中文有问题
import sys
import xlwt  #写入excel表的模块包
reload(sys)
sys.setdefaultencoding('utf8')

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.Qt import *
from Ui_main_widget import Ui_Form
import jobDB
import apriori
import re
import Queue
import random
import spider
import threading
#from push_button import *
from Login import login  #登录窗口
import time
from bloomFilter import bloomfilter  #judge the job is saved or not

mutex = threading.RLock() #the thread lock be used synchronization
bFilter = bloomfilter.BloomFilter('./bloomFilter/jobHash.txt')

apr = apriori.apriori()
db = jobDB.jobDB()

######这个部分是爬虫部分了#####很重要。本来我是单独写在另外一个文件的。但#是发现引用过来的时候。不能返回信号给另外一个线程。所以只好重新改写，然后##放在这个文件你。

class connectNetwork(QThread): 
    networkUpdated=pyqtSignal(str) 
    def __init__(self,work_num=20,thread_num=5): 
        QThread.__init__(self) #没有parent参数 
        self.connect_newtwork_spider = spider.jobSpider()
        self.moveToThread(self) 
        self.myHref = 0
        self.timeout = 10
    def run(self):
        #self.progressUpdated.emit('start') 
        print 'isFinished =',self.isFinished
        while True:
            self.timeout = 10  #如果获取10次都失败，就提示用户电脑是否已经连网！
            while self.myHref == 0:
                self.myHref = self.connect_newtwork_spider.judge_is_connect_network('http://www.baidu.com') 
                #print 'self.myHref =',self.connect_newtwork_spider.judge_is_connect_network('http://www.baidu.com')
                self.timeout -= 1
                print 'timeout =',self.timeout
                if self.timeout <= 0:
                    self.networkUpdated.emit(u'网络已经断开') 
                    time.sleep(1)
                    #print 'countPage = 失败 ' ,self.countPage
                    self.tiemout = 10 
            self.timeout = 20   #已经成功获取信息，则复原 connectTime 的值
            self.networkUpdated.emit(u'网络已经连接') 
            print 'lianjie'
            self.myHref = 0
            time.sleep(5)

#####下面是线程池用到的类或者函数######

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

"""
爬虫线程池函数  和上面的类 work 是一起使用的。不用另外一个线程的话，当启动爬虫时，其他功能就无法操作了。因为单线程必须要等待一个操作完成之后才能做另外一个操作，但是爬虫是可以无限爬下去的。所以决定用另外一个线程来让他单独工作
"""

class ProcessorThread(QThread): 
    progressUpdated=pyqtSignal(str) 
    def __init__(self,work_num=20,thread_num=5): 
        QThread.__init__(self) #没有parent参数 
        self.jobhref_spider = spider.jobSpider()
        self.countThread = 1   # count the number Thread
        self.countPage = 1     #cout the number of page
        self.myHref = 0   # judge 'myHref' is none or not
        self.countJob= 1
        #self.countAddJob = 2
        #self.myThreadPool = workManager.WorkManager(200,5)
	#self.myThreadPool = WorkManager(200,5)

        self.isFinished = False    	
        self.firstCrawler = True

	self.work_queue = Queue.Queue()
        self.threads = []
        self.work_num = work_num
        self.thread_num = thread_num
        self.notNetwork =  10 #如果两10次都连不上的话，提示客户网络是否已经断开 
        self.moveToThread(self) 
	
    """
    初始化线程
    """
    #def my__init_thread_pool(self):
    ##def __init_thread_pool(self):
    #    for i in range(self.thread_num):
    #        self.threads.append(Work(self.work_queue))
    #    #return "test return workManager.py + '\n\n\n\n\n\n'"
    
    def my__init_thread_pool(self):
        for i in range(self.thread_num):
            self.threads.append(Work(self.work_queue))



    def my__init_work_queue(self, href = 'testUrl',countJob = 1):
        #for i in range(jobs_num):
        self.add_job(self.do_job, href,countJob)
	print 'counJob =',countJob
    
    #添加任务
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))#任务入队，Queue内部实现了同步机制

    #返回线程池任务队列中的任务数量
    def check_queue(self):
        return self.work_queue.qsize()

    #等待所有的线程结束
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

    
    def do_job(self,args):
        #while self.isFinished is True:
        #while self.isFinished is False:  #这个是按暂停按钮时运行这个循环，直到按开始按钮之后才会执行下面的程序
        #    pass

        print 'function do_job() start...'
        time.sleep(random.randint(2,5))#模拟处理时间
        #print "countJob(args[1]) = " , args[1]        
        count = args[1]
        print 'count =',count
        print 'coutnt = ',count
        mainSpider = spider.jobSpider()
        href = args[0]
        #self.progressUpdated.emit(u'开始存储岗位基本信息.\n')
        if bFilter.isContaions(href) == False:
            if mainSpider.get_jobs(href) == 1:     #获取信息成功
                bFilter.insert(href)   #做标记，已经存了
                mutex.acquire()      #lock.in order to synchronization 
                
		#self.progressUpdated.emit('start saving datas.')
                print '开始存储岗位基本信息\n'                
                jobInfo = mainSpider.save_data()
                print 'satrt saving................................................................................'
                #self.progressUpdated.emit(u'开始存储岗位基本信息.\n' + jobInfo)
                self.progressUpdated.emit(u"第" + str(count) +u"条岗位信息。" + u'开始存储岗位基本信息到数据库中.\n' + jobInfo)
                print '开始存储课程集合和地点############################################333 \n'
                mainSpider.save_job_course_set_and_workplace()
                self.progressUpdated.emit(u"第" + str(count) +u"条岗位信息。" + u'开始存储课程集合和地点到文件中.')

                mutex.release()      #unlock
        else:
            self.progressUpdated.emit( u"第" + str(count) +u"条岗位信息。" + href + u",已经存储和处理过了。" )
            #print '%s the job has exists' % href
        print threading.current_thread(), list(args)
    
    #线程开始之后执行的函数
    def run(self):
	#self.progressUpdated.emit('start') 
        print 'isFinished =',self.isFinished
        while self.check_queue() >=0 and self.check_queue() <= 10 and self.isFinished is True:
            print 'myThreadPool.check_queue() ' , self.check_queue() ,'isFinished',self.isFinished
            #self.countAddJob += 1
            #print 'countJob = ' , self.countJob
            self.myHref = 0
            connectTime = 10  #如果获取10次都失败，就提示用户电脑是否已经连网！
            while self.myHref == 0 and self.isFinished is True: 
                self.myHref = self.jobhref_spider.get_first_jobhref(self.countPage)
                connectTime -= 1
                if self.myHref == 0 :
	            self.progressUpdated.emit(u'尝试连接网络中......') 
                if connectTime == 0:
	            self.progressUpdated.emit(u'请查看你的网络是否已经连接======') 
                    time.sleep(2)
                    #print 'countPage = 失败 ' ,self.countPage
	            connectTime = 10 
	    connectTime = 10   #已经成功获取信息，则复原 connectTime 的值
            #print '成功获取url ',
            #print 'isFinished =',self.isFinished
            self.countPage += 1	
            for href in self.myHref:     #把url加入到任务队列中
                if self.isFinished is True:
                    #print 'isFinished =',self.isFinished
                    self.my__init_work_queue(href,self.countJob)
		    #self.progressUpdated.emit("add href" + str(self.countJob)) 
                    print 'self.countJob =',self.countJob
                    self.countJob += 1

            self.countThread += 1	 
            if self.firstCrawler is True:
                self.my__init_thread_pool()
                self.firstCrawler = False
            	#self.progressUpdated.emit("firstCrawler") 

#列表内容区中显示
class CenterDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
    def paint(self, painter, option, index):
        painter.save()
        #painter.drawText(option.rect, Qt.AlignCenter, index.data(Qt.DisplayRole).toString())
	painter.drawText(option.rect, Qt.TextWordWrap | Qt.AlignHCenter, index.data(Qt.DisplayRole).toString())        
	painter.restore()

#主窗口类
class Pyqtdemo(QtGui.QWidget, Ui_Form):
    """
    主窗口，由于刚刚学习pyqt，而且时间关系,完善窗口代码没有做优化，所以这里有很多重复的代码
    """
    def __init__(self, parent = None):
        """
        构造函数
        """
        self.apriori_result = [] #保存关联分析的结果
        self.apriori_search_x = [] #保存关联分析之后，搜索前项 x 的保存结果
        self.apriori_search_y = [] #保存关联分析之后，搜索后项 y 的保存结果
        self.popCourse = [] #保存课程热度的列表
        self.popWorkplace = [] #保存岗位地点的热度列表
        self.analysis_type = '' #分析数据的类别 
        self.job_type = ''#要分析的工作类别 
        
        ### 
        self.associate_analysis_support = 0.05  #关联分析的支持度
        self.associate_analysis_confidence = 0.005  #关联分析的置信度

        #self.admin_login
	self.model = QtGui.QStandardItemModel()	
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.setFixedSize(self.width(),self.height())   #固定大小
	self.setFixedHeight(self.height()) 	
	self.tool_button_background()        
	self.tbl_job_details.setItemDelegate(CenterDelegate())       
	self.center()    #窗口区中
        self.init_other_widget()
	self.label_job_type_num.setStyleSheet("color:white")        
	self.label_job_type_num_widget2.setStyleSheet("color:white") 
	self.label_job_analysis_num_widget2.setStyleSheet("color:white") 
	self.mouse_press = False
	self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget) #设置窗口类型  无边框
        self.isFirstStartThread = True 
        #self.btn_modify_support_and_confidence.setEnabled(False)

	#这个部分是线程池
	self.processorThread=ProcessorThread(200,3)  #可以同时200个任务。有3个线程组成的线程池
        self.processorThread.progressUpdated.connect(self.updateProgress, Qt.QueuedConnection) 	
        
        #这个部分是判断是否连接网络的线程
        #self.conNetwork = connectNetwork()
        ##连接信号槽
        #self.conNetwork.networkUpdated.connect(self.updateNetwork,Qt.QueuedConnection)
        #self.conNetwork.start()
	self.initTitle()    ################################################	

    @pyqtSlot(str) 
    def updateProgress(self, value): 
	self.listWidget.addItem(value)	
	countItem = self.listWidget.count()        
	self.listWidget.setCurrentRow(countItem)

    @pyqtSlot(str) 
    def updateNetwork(self, value): 
        self.label_connect_network.setText(value)

    def initTitle(self):
	#self.title_label =  QtGui.QLabel(self) 
	self.title_label.setText(u"桂智网络招聘岗位分析软件 V1.0")
        #self.label_logo =  QtGui.QLabel(self)
        #self.close_button =  QtGui.QPushButton(self)

        title_pixmap = QPixmap ("./img/toolButton/logo.png")
        self.label_logo.setPixmap(title_pixmap)
        self.label_logo.setFixedSize(66, 66)
        self.label_logo.setScaledContents(True)
       
	#self.setFixedSize(self.btn_width, self.btn_height)
        self.title_label.setFixedHeight(30)
	
        self.title_label.setStyleSheet("color:white")
        self.connect(self.close_button, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
	#self.connect(self.minimize_button, QtCore.SIGNAL("clicked()"),QtCore.SLOT("showMinimized()"))
	
	QtCore.QObject.connect(self.minimize_button, QtCore.SIGNAL("clicked()"), self.showMinimized)
    
    #窗口区中显示
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def mousePressEvent(self,event ):
	#只能是鼠标左键移动和改变大小
	if(event.button() == Qt.LeftButton): 
	    self.mouse_press = True
	    #窗口移动距离
	    self.move_point = event.globalPos() - self.pos() 
	
	
    def mouseReleaseEvent(self,event):
	self.mouse_press = False        

    #移动窗口
    def mouseMoveEvent(self,event):
	
	if(self.mouse_press):   
            self.move_pos = event.globalPos()
            self.move(self.move_pos - self.move_point)

    #设置背景颜色和图片	
    def paintEvent(self, event):
             
        self.painter = QtGui.QPainter()
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), QPixmap("./img/skin/17_big.png"))
        self.painter.end()
        linear2 = QLinearGradient(QtCore.QPoint(self.rect().topLeft()), QtCore.QPoint(self.rect().bottomLeft()))
        linear2.start()
        linear2.setColorAt(0, Qt.white)
        linear2.setColorAt(0.5, Qt.white)
        linear2.setColorAt(1, Qt.white)
        linear2.finalStop()
        self.painter2 = QtGui.QPainter()
        self.painter2.begin(self)
        self.painter2.setPen(Qt.white) #设定画笔颜色，到时侯就是边框颜色
        self.painter2.setBrush(linear2);
        self.painter2.drawRect(QRect(0, 80, self.width(), self.height() - 30));
        self.painter2.end()
        
    #初始化其他窗口，下拉框	
    def init_other_widget(self):
        # 1
        job_type_list = [u'------岗位类别-------',u'全部岗位',u'IOS',u'Android',u'Python',u'Java',u'C++',u'C#',u'.Net',u'测试',u'数据分析',u'数据库',u'架构师',u'UI',u'游戏',u'网页设计',u'网站',u'安全',u'运维',u'Perl',u'Ruby',u'Hadoop',u'Node.js',u'Php']
	for jt in job_type_list:
	    self.cmbx_job_type.addItem(jt)
        #self.connect(self.cmbx_job_type, QtCore.SIGNAL(self.currentIndexChanged(int)), this, QtCore.SLOT(self.comboBoxValueChanged())) 
	#self.connect(self.cmbx_job_type, QtCore.SIGNAL(self.cmbx_job_type.currentIndexChanged(int)), self.my_comboBox)
	
	self.connect(self.cmbx_job_type, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboBoxValueChanged_job_details)

        # 2 
        search_item = [u'-----选择搜索项---------',u'公司名称',u'岗位名称',u'岗位地点']
        for si in search_item:
            self.cmbx_search_item_widget1.addItem(si)

        # 3
        #这个部分是初始化下拉框 cmbx_analysis_type的选项 
        analysis_type_list = [u'------分析类别-----------',u'单门课程热度',u'岗位地点热度',u'课程关联分析']
        for at in analysis_type_list:
            self.cmbx_analysis_type.addItem(at)
        
        
	self.connect(self.cmbx_analysis_type, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboBoxValueChanged_analysis_type)
        # 4
        #这个部分是初始化下拉框cmbx_job_type_in_analysis的选项 
        job_type_analysis_list =   [u'------岗位类别------------',u'全部岗位',u'IOS',u'Android',u'Python',u'Java',u'C++',u'C#',u'.Net',u'测试',u'数据分析',u'数据库',u'架构师',u'UI',u'游戏',u'网页设计',u'网站',u'安全',u'运维',u'Perl',u'Ruby',u'Hadoop',u'Node.js',u'Php']

	for jt in job_type_analysis_list:
	    self.cmbx_job_type_in_analysis.addItem(jt)
        self.cmbx_job_type_in_analysis.setMaxVisibleItems(10) 
	
	
	self.connect(self.cmbx_job_type_in_analysis, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboBoxValueChanged_job_type)


        # 5
        # 这个部分是初始化下拉框cmbx_support 和 cmbx_confidence 的选项 
        supp_and_conf_list = [u'0.']
        
        for sc in supp_and_conf_list:
            self.cmbx_support.addItem(sc)
            self.cmbx_confidence.addItem(sc)
        
################################stackedWidgetPage1 函数区域  111111111111111111111111111111111111111111111111111111111111
    #def comboBoxValueChanged(self):
    def comboBoxValueChanged_job_details(self):
        print 'comboBoxValueChanged_job_details'
        comText = self.cmbx_job_type.itemText(self.cmbx_job_type.currentIndex())
        print type(comText)
        #QtCore.QByteArray toUtf8(comText)
        qbyte = unicode(comText)
        print 'index =',self.cmbx_job_type.currentIndex() 
        if self.cmbx_job_type.currentIndex() == 1:
            self.load_data()
        else:
            print 'qbyte=',type(qbyte)
            print 'comText=',qbyte

            self.load_data_by_cmbx_job_type(qbyte)    #把查询到的数据导入到table的函数 
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
           u"真的要退出?", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    

#导入数据到tableview中
    def load_data(self):
        #先清空
        self.ledit_position_count_widget1.setText('')	

        self.model.clear()
        self.tbl_job_details.clearSpans()

	job_details = db.query_job_details()
	#self.model.setHorizontalHeaderLabels(['company', 'position','release_date', 'education', 'workplace','salary', 'years_of_work', 'the_num_of_recuritment', 'description','url'])
	self.model.setHorizontalHeaderLabels([u'公司', u'岗位',u'发布日期', u'教育背景', u'工作地点',u'薪水', u'工作年限要求', u'需签约年限', u'岗位需求和要求',u'岗位URL'])
	#for i in range(20):
	#    testData = QtGui.QStandardItem("Tom")	
	#    self.model.setItem(i,0,testData)
	#self.tbl_job_details.setModel(self.model)
        count_job_num = 0
	for details in job_details:
            #if count_job_num == 10:
            #    break
            column = 0
            for det in details:
                if cmp(det.encode('utf-8'),'') == 0 and column == 0:  #cmp(str(type(det)),"<type 'datetime.date'>") == 0:
                    break
                else:
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_job_num,column,testData)
                    column = column + 1
                    #print 'column=',column
                    #print 'det =',det
            count_job_num = count_job_num + 1
        #testData = QtGui.QStandardItem("nihao\nhasdf \n")
        #self.model.setItem(count_job_num,column,testData)
	self.tbl_job_details.setModel(self.model)
        self.ledit_position_count_widget1.setText(str(count_job_num))	
    #按工作类型输出原始数据
    def load_data_by_cmbx_job_type(self,query_job_type = ''):
        #先清空
        self.ledit_position_count_widget1.setText('')	

        self.model.clear()
	self.tbl_job_details.clearSpans()

        job_details = db.query_job_details_by_position(query_job_type)
	#self.model = QtGui.QStandardItemModel()	
	self.model.setHorizontalHeaderLabels([u'公司', u'岗位',u'发布日期', u'教育背景', u'工作地点',u'薪水', u'工作年限要求', u'需签约年限', u'岗位需求和要求',u'岗位URL'])
        count_job_num = 0
	for details in job_details:
            #if count_job_num == 10:
            #    break
            column = 0
            for det in details:
                if cmp(det.encode('utf-8'),'') == 0 and column == 0:  #cmp(str(type(det)),"<type 'datetime.date'>") == 0:
                    break
                else:
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_job_num,column,testData)
                    column = column + 1
            count_job_num = count_job_num + 1
	self.tbl_job_details.setModel(self.model)
        self.ledit_position_count_widget1.setText(str(count_job_num))	
	self.tbl_job_details.resizeRowsToContents()

    def search_data_by_cmbx_search_item_widget1(self,search_item_contend = '',condition = ''):

        #先清空
        self.ledit_position_count_widget1.setText('')	

        if cmp(search_item_contend,'公司名称') == 0:
            job_details = db.query_job_details_by_company(condition)
        elif cmp(search_item_contend,'岗位名称') == 0:
            job_details = db.query_job_details_by_position(condition)
        else:
            job_details = db.query_job_details_by_workplace(condition)


        self.model.clear()
	self.tbl_job_details.clearSpans()
	#self.model = QtGui.QStandardItemModel()	
	self.model.setHorizontalHeaderLabels([u'公司', u'岗位',u'发布日期', u'教育背景', u'工作地点',u'薪水', u'工作年限要求', u'需签约年限', u'岗位需求和要求',u'岗位URL'])
        count_job_num = 0
	for details in job_details:
            #if count_job_num == 10:
            #    break
            column = 0
            for det in details:
                if cmp(det.encode('utf-8'),'') == 0 and column == 0:  #cmp(str(type(det)),"<type 'datetime.date'>") == 0:
                    break
                else:
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_job_num,column,testData)
                    column = column + 1
            count_job_num = count_job_num + 1
	self.tbl_job_details.setModel(self.model)

        #显示该类岗位的总数
        self.ledit_position_count_widget1.setText(str(count_job_num))

################################stackedWidgetPage2 函数区域22222222222222222222222222222222222222222222222222222
    

    #这个函数包含你太多的分析，可能会有点混乱
    def comboBoxValueChanged_job_type(self):
        #不可点击修改支持度和置信度的按钮

        #self.btn_modify_support_and_confidence.setEnabled(False)
        analysisType = self.cmbx_analysis_type.currentIndex()
        jobType = self.cmbx_job_type_in_analysis.currentIndex()
        comText_analysisType = self.cmbx_analysis_type.itemText(analysisType)
        comText_analysisType = unicode(comText_analysisType)
        comText_analysisType = comText_analysisType.encode('utf-8')

        comText_jobType = self.cmbx_job_type_in_analysis.itemText(jobType)
        comText_jobType = unicode(comText_jobType)
        comText_jobType = comText_jobType.encode('utf-8')
        print type(comText_jobType)
        #print "analysis_type =",comText_analysisType
        print 'cmbx_analysis_type Num = ',self.cmbx_analysis_type.currentIndex()
        print 'cmbx_job_type Num = ',self.cmbx_job_type_in_analysis.currentIndex()
        #if self.cmbx_analysis_type.currentIndex() != 0 and self.cmbx_job_type_in_analysis.currentIndex() != 0:  #如果没有岗位选择类别或者没有变化时
        print 'testst'
        if analysisType != 0 and jobType != 0:
            print comText_jobType
            if cmp(comText_analysisType,'单门课程热度') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + comText_jobType + ".txt"
                    self.pop_course(fileName)            
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + "Net" + ".txt"
                    self.pop_course(fileName)            
                else:
                    fileName = "./save_analysis_result/apriori_course_result/" + "NodeJs" + ".txt"
                    self.pop_course(fileName)            
                
            if cmp(comText_analysisType,'岗位地点热度') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = "./save_analysis_result/workplace_result/" + comText_jobType + ".txt"
                    self.pop_workplace(fileName)            
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/workplace_result/" + "Net" + ".txt"
                    self.pop_workplace(fileName)            
                else:
                    fileName = "./save_analysis_result/workplace_result/" + "NodeJs" + ".txt"
                    self.pop_workplace(fileName)            

            if cmp(comText_analysisType,'课程关联分析') == 0:

                #让修改支持度和置信度的确定按钮可以使用
                #self.btn_modify_support_and_confidence.setEnabled(True)
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + comText_jobType + ".txt"
                    self.apriori_course(fileName)            
                    print 'fn',fileName
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + "Net" + ".txt"
                    self.apriori_course(fileName)            
                    print 'fn',fileName
                else:
                    fileName = "./save_analysis_result/apriori_course_result/" + "NodeJs" + ".txt"
                    self.apriori_course(fileName)            
                    print 'fn',fileName
        
    

    ######        
    def comboBoxValueChanged_analysis_type(self):
        #不可点击修改支持度和置信度的按钮
        #self.btn_modify_support_and_confidence.setEnabled(False)
        #if self.cmbx_analysis_type.currentIndex() != 0 and self.cmbx_job_type_in_analysis.currentIndex() != 0: #如果没有岗位选择类别或者没有变化时
        analysisType = self.cmbx_analysis_type.currentIndex()
        jobType = self.cmbx_job_type_in_analysis.currentIndex()
        comText_analysisType = self.cmbx_analysis_type.itemText(analysisType)
        comText_analysisType = unicode(comText_analysisType)
        #comText_analysisType = comText_analysisType.encode('utf-8')

        comText_jobType = self.cmbx_job_type_in_analysis.itemText(jobType)
        comText_jobType = unicode(comText_jobType)
        #comText_jobType = comText_jobType.encode('utf-8')

        if analysisType != 0 and jobType != 0:
            print comText_jobType
            if cmp(comText_analysisType,'单门课程热度') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + comText_jobType + ".txt"
                    self.pop_course(fileName)            
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + "Net" + ".txt"
                    self.pop_course(fileName)            
                else:
                    fileName = "./save_analysis_result/apriori_course_result/" + "NodeJs" + ".txt"
                    self.pop_course(fileName)            
                
            if cmp(comText_analysisType,'岗位地点热度') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = "./save_analysis_result/workplace_result/" + comText_jobType + ".txt"
                    self.pop_workplace(fileName)            
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/workplace_result/" + "Net" + ".txt"
                    self.pop_workplace(fileName)            
                else:
                    fileName = "./save_analysis_result/workplace_result/" + "NodeJs" + ".txt"
                    self.pop_workplace(fileName)            

            if cmp(comText_analysisType,'课程关联分析') == 0:
                #让修改支持度和置信度的确定按钮可以使用
                #self.btn_modify_support_and_confidence.setEnabled(True)

                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + comText_jobType + ".txt"
                    self.apriori_course(fileName)            
                    print 'fn',fileName
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/apriori_course_result/" + "Net" + ".txt"
                    self.apriori_course(fileName)            
                    print 'fn',fileName
                else:
                    fileName = "./save_analysis_result/apriori_course_result/" + "NodeJs" + ".txt"
                    self.apriori_course(fileName)            
                    print 'fn',fileName

    #这个函数是关于岗位地点的频率的高低统计
    def pop_workplace(self,filename):
        #先清空数据
        self.ledit_position_count_widget2.setText('')
        self.ledit_analysis_result_count_widget2.setText('')

        position_count = 0
        self.model.clear()
        self.tbl_anaysis_result.clearSpans()
	
        self.model.setHorizontalHeaderLabels([ u'地点',u'频率'])
        self.popWorkplace , position_count = apr.analysis_popular_workplace(filename)
        #print 'self.popWorkplace',self.popWorkplace
        count_analysis_count = 0
        for details in self.popWorkplace: 
            #if count_job_num == 1:
            #    break
            column = 0
            for det in details:
                if column <= 0:
                    #det = "%.4f" % det
                    det = unicode(det,'utf-8')
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_analysis_count,column,testData)
                    column = column + 1
                else:
                    det = "%.4f" % det
                    det = unicode(det)
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_analysis_count,column ,testData)  #column 要 减去 1
            count_analysis_count = count_analysis_count + 1

        #把相应的岗位总数，分析的结果总数，显示在相应的地方
        self.ledit_position_count_widget2.setText(str(position_count))
        self.ledit_analysis_result_count_widget2.setText(str(count_analysis_count))

	self.tbl_anaysis_result.setModel(self.model)
        self.tbl_anaysis_result.setColumnWidth(0,289)
        self.tbl_anaysis_result.setColumnWidth(1,289)

    #这个函数是关于课程地点的频率的高低统计
    def pop_course(self,filename):
        #先清空数据
        self.ledit_position_count_widget2.setText('')
        self.ledit_analysis_result_count_widget2.setText('')
        position_count = 0
        
        self.model.clear()
        self.tbl_anaysis_result.clearSpans()
	
        self.model.setHorizontalHeaderLabels([ u'课程',u'频率'])
        self.popCourse , position_count = apr.analysis_popular_course(filename)
        count_analysis_count = 0
        for details in self.popCourse: 
            #if count_job_num == 1:
            #    break
            column = 0
            for det in details:
                if column <= 0:
                    #det = "%.4f" % det
                    det = unicode(det,'utf-8')
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_analysis_count,column,testData)
                    column = column + 1
                else:
                    det = "%.4f" % det
                    det = unicode(det)
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_analysis_count,column ,testData)  #column 要 减去 1
            count_analysis_count = count_analysis_count + 1


        #把相应的岗位总数，分析的结果总数，显示在相应的地方
        self.ledit_position_count_widget2.setText(str(position_count))
        self.ledit_analysis_result_count_widget2.setText(str(count_analysis_count))

	self.tbl_anaysis_result.setModel(self.model)
        self.tbl_anaysis_result.setColumnWidth(0,289)
        self.tbl_anaysis_result.setColumnWidth(1,289)
    
    #这个函数是关于岗位地点的 关联分析函数
    def apriori_course(self,filename = ''):
        #先清空数据
        self.ledit_position_count_widget2.setText('')
        self.ledit_analysis_result_count_widget2.setText('')
        position_count = 0
        self.model.clear()
        self.tbl_anaysis_result.clearSpans()
        self.apriori_result = ''
        self.apriori_result , position_count = apr.apriori_course(filename ,self.associate_analysis_support ,self.associate_analysis_confidence)
        #for ar in self.apriori_result:
        #    for a in ar:
        #        print 'a =',a,
        #    print '' 
        #print 'print Done.'
        self.model.setHorizontalHeaderLabels([u'支持度', u'置信度',u'具体内容 X-->Y '])
        count_analysis_count = 1  #不能删除，很关键，是插入第几行的
        self.model.setItem(0,0,QtGui.QStandardItem(unicode(self.associate_analysis_support)))
        self.model.setItem(0,1,QtGui.QStandardItem(unicode(self.associate_analysis_confidence)))
        self.model.setItem(0,2,QtGui.QStandardItem(u'此次课程关联分析的置信度和支持度的阈值'))
        for details in self.apriori_result: 
            #print 'countjN',count_analysis_count ,'details=',details
            #if count_job_num == 1:
            #    break
            merge_x_y = ''
            column = 0
            for det in details:
                if column <= 1:
                    #det = "%.4f" % det
                    det = unicode(det)
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_analysis_count,column,testData)
                    column = column + 1
                elif column == 2:
                    det = unicode(det,'utf-8')
                    merge_x_y = merge_x_y + det + '-->'
                    #print 'merge_x_y 11=',merge_x_y
                    column = column + 1
                else:
                    det = unicode(det,'utf-8')
                    det = merge_x_y + det 
                    #print 'merge_x_y 22=',det
                    testData = QtGui.QStandardItem(det)
                    self.model.setItem(count_analysis_count,column - 1,testData)  #column 要 减去 1
            count_analysis_count = count_analysis_count + 1

        #把相应的岗位总数，分析的结果总数，显示在相应的地方
        self.ledit_position_count_widget2.setText(str(position_count))
        self.ledit_analysis_result_count_widget2.setText(str(count_analysis_count))
        self.tbl_anaysis_result.setModel(self.model)
        self.tbl_anaysis_result.setColumnWidth(0,88)
        self.tbl_anaysis_result.setColumnWidth(1,88)
        self.tbl_anaysis_result.setColumnWidth(2,410)
        self.tbl_anaysis_result.resizeRowsToContents()
        

    #设置job_details_button的背景图片和样式
    def tool_button_background(self):
    	self.job_details_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/file.png")
	self.job_details_button.setIcon(QIcon(recovery_pixmap))
	self.job_details_button.setIconSize(recovery_pixmap.size())
	self.job_details_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	self.job_details_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	#设置job_analysis_button 的背景图片和样式
	self.job_analysis_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/analysis.png")
	self.job_analysis_button.setIcon(QIcon(recovery_pixmap))
	self.job_analysis_button.setIconSize(recovery_pixmap.size())
	self.job_analysis_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	self.job_analysis_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
    	
	#设置crawler_job_button 的背景图片和样式
	self.crawler_job_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/spider11.png")
	self.crawler_job_button.setIcon(QIcon(recovery_pixmap))
	self.crawler_job_button.setIconSize(recovery_pixmap.size())
	self.crawler_job_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	self.crawler_job_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
      

	#设置connect_us_button 的背景图片和样式
	self.connect_us_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/emil4.png")
	self.connect_us_button.setIcon(QIcon(recovery_pixmap))
	self.connect_us_button.setIconSize(recovery_pixmap.size())
	self.connect_us_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	self.connect_us_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")


	self.tool_btn_search.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/search4.png")
	self.tool_btn_search.setIcon(QIcon(recovery_pixmap))
	self.tool_btn_search.setIconSize(recovery_pixmap.size())
	self.tool_btn_search.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 0)
	self.connect_us_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")

        #self.close_button.loadPixmap("./img/sysButton/close.png")
	#设置close_button 的背景图片和样式
	self.close_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/close.png")
	self.close_button.setIcon(QIcon(recovery_pixmap))
	self.close_button.setIconSize(recovery_pixmap.size())
	self.close_button.setFixedSize(recovery_pixmap.width() + 25, recovery_pixmap.height() + 15)
	#self.connect_us_button.setStyleSheet("QToolButton{background:transparent}"
	#	"QToolButton:hover{border-radius:5px;border:1px solid rgb(110, 190, 10)}")
	self.close_button.setStyleSheet("background:transparent")
	self.close_button.setToolTip(u"退出")   #鼠标在他上面时的提示

	#设置minimize_button 的背景图片和样式
	self.minimize_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/minimize.png")
	self.minimize_button.setIcon(QIcon(recovery_pixmap))
	self.minimize_button.setIconSize(recovery_pixmap.size())
	self.minimize_button.setFixedSize(recovery_pixmap.width() + 25, recovery_pixmap.height() + 15)
	self.minimize_button.setStyleSheet("background:transparent")
	self.minimize_button.setToolTip(u"最小化")   #鼠标在他上面时的提示
	#self.connect(self.minimize_button, SIGNAL("showMin()"), self, SLOT("showMinimized()"))	

	#设置start_crawler_job_button 的背景图片和样式
	self.start_crawler_job_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/startCrawler4.png")
	self.start_crawler_job_button.setIcon(QIcon(recovery_pixmap))
	self.start_crawler_job_button.setIconSize(recovery_pixmap.size())
	self.start_crawler_job_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	self.start_crawler_job_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")

	#设置stop_crawler_job_button 的背景图片和样式
	self.stop_crawler_job_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/stopCrawler.png")
	self.stop_crawler_job_button.setIcon(QIcon(recovery_pixmap))
	self.stop_crawler_job_button.setIconSize(recovery_pixmap.size())
	self.stop_crawler_job_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	self.stop_crawler_job_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
    
    #导出热门课程到execl表中
    def export_execl_pop_courese(self,fileName = ''): 
        file_execl = xlwt.Workbook()
        table = file_execl.add_sheet('sheet1',cell_overwrite_ok = True)
        table.write(0,0,u'课程')
        table.write(0,1,u'频率')
        count_analysis_count = 1
        for details in self.popCourse: 
            column = 0
            for det in details:
                if column <= 0:
                    det = unicode(det,'utf-8')
                    table.write(count_analysis_count,column,det)
                    column = column + 1
                else:
                    det = "%.4f" % det
                    det = unicode(det)
                    table.write(count_analysis_count,column,det)
            count_analysis_count = count_analysis_count + 1
        #保存文件
        file_execl.save(fileName)
        #file_execl.save('/home/lvchuan/python/IOS.xls')

    #导出热门岗位地点到execl表中
    def export_execl_pop_workplace(self,fileName = ''): 
        file_execl = xlwt.Workbook()
        table = file_execl.add_sheet('sheet1',cell_overwrite_ok = True)
        table.write(0,0,u'岗位工作地点')
        table.write(0,1,u'频率')
        count_analysis_count = 1
        for details in self.popWorkplace: 
            column = 0
            for det in details:
                if column <= 0:
                    #det = "%.4f" % det
                    det = unicode(det,'utf-8')
                    table.write(count_analysis_count,column,det)
                    column = column + 1
                else:
                    det = "%.4f" % det
                    det = unicode(det)
                    table.write(count_analysis_count,column,det)
            count_analysis_count = count_analysis_count + 1

        #保存文件
        file_execl.save(fileName)

    #导入课程关联分析结果到execl中
    def export_execl_apriori_course(self,fileName = ''):
        file_execl = xlwt.Workbook()
        table = file_execl.add_sheet('sheet1',cell_overwrite_ok = True)
        table.write(0,0,u'支持度')
        table.write(0,1,u'置信度')
        table.write(0,2,u'具体内容 X-->Y ')
        table.write(1,0,unicode(self.associate_analysis_support))
        table.write(1,1,unicode(self.associate_analysis_confidence))
        table.write(1,2,u'此次课程关联分析的置信度和支持度的阈值')
        count_analysis_count = 2  #不能删除，很关键，是插入第几行的
        for details in self.apriori_result: 
            merge_x_y = ''
            column = 0
            for det in details:
                if column <= 1:
                    det = unicode(det)
                    table.write(count_analysis_count,column,det)
                    column = column + 1
                elif column == 2:
                    det = unicode(det,'utf-8')
                    merge_x_y = merge_x_y + det + '-->'
                    column = column + 1
                else:
                    det = unicode(det,'utf-8')
                    det = merge_x_y + det 
                    table.write(count_analysis_count,column-1,det)
            count_analysis_count = count_analysis_count + 1

        #保存文件
        file_execl.save(fileName)


    #第一个页面搜索按钮的函数 btn_search 
    @QtCore.pyqtSignature("")
    def on_tool_btn_search_clicked(self):
        search_item_num = self.cmbx_search_item_widget1.currentIndex()
        search_item_contend = self.cmbx_search_item_widget1.itemText(search_item_num)
        search_item_contend = unicode(search_item_contend)
        #search_item_contend = search_item_contend.encode('utf-8')
        if search_item_num == 0:
            reply = QtGui.QMessageBox.question(self, 'Message',
               u"请选择搜索项", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        elif cmp(search_item_contend,'公司名称') == 0:
            condition = unicode(self.ledit_search.text())
            #print 'condition =',condition
            #print 'sic =',search_item_contend
            self.search_data_by_cmbx_search_item_widget1(search_item_contend,condition)
        elif cmp(search_item_contend,'岗位名称') == 0:
            condition = unicode(self.ledit_search.text())
            #print 'condition =',condition
            #print 'sic =',search_item_contend
            self.search_data_by_cmbx_search_item_widget1(search_item_contend,condition)
        else:
            condition = unicode(self.ledit_search.text())
            #print 'condition =',condition
            #print 'sic =',search_item_contend
            self.search_data_by_cmbx_search_item_widget1(search_item_contend,condition)

    
    ############################
    #这部分是按钮信号重载的地方#
    ############################
    @QtCore.pyqtSignature("")
    def on_job_details_button_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    @QtCore.pyqtSignature("")
    def on_job_analysis_button_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    @QtCore.pyqtSignature("")
    def on_crawler_job_button_clicked(self):
        self.admin_login = login.login()    
        #self.admin_login.show()
        #self.admin_login.exec_()
        if self.admin_login.exec_() == QtGui.QDialog.Accepted:
            self.stackedWidget.setCurrentIndex(2)	

    @QtCore.pyqtSignature("")
    def on_connect_us_button_clicked(self):
        self.stackedWidget.setCurrentIndex(3)	

    #搜索关联规则前项 btn_the_course_search_widget2

	
    @QtCore.pyqtSignature("")
    def on_btn_the_course_search_widget2_clicked(self): 
	analysisType = self.cmbx_analysis_type.currentIndex()
        jobType = self.cmbx_job_type_in_analysis.currentIndex()
        comText_analysisType = self.cmbx_analysis_type.itemText(analysisType)
        comText_analysisType = unicode(comText_analysisType)
        #comText_analysisType = comText_analysisType.encode('utf-8')


	if cmp(comText_analysisType,'课程关联分析') != 0:
            #reply = QtGui.QMessageBox.question(self, 'Message',
            #   u"目前不是课程关联分析，不能使用该功能！", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            reply = QtGui.QMessageBox.question(self, 'Message',
               u"目前不是课程关联分析，不能使用该功能！", QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                #event.accept()
                pass
            else:
                #event.ignore()
                pass
        
	else:
            self.tbl_anaysis_result.clearSpans()
            apriori_x = unicode(self.ledit_the_former.text())
            apriori_y = unicode(self.ledit_the_latter.text())
            self.apriori_search_x = [] #清空数据
            self.apriori_search_y = [] #清空数据
            print 'apriori_x =',apriori_x
            print 'apriori_y =',apriori_y
            if cmp(apriori_x,'') == 0:
                self.apriori_search_x = self.apriori_result  #把原始的关联分析复制给 apriori_search_x
            else:
                apriori_x = apriori_x.encode('utf-8')
                self.model.clear()    
                self.model.setHorizontalHeaderLabels([u'支持度', u'置信度',u'具体内容 X-->Y '])
                #print 'start loading'
                count_job_num = 0
                for details in self.apriori_result: 
                    if re.search(apriori_x,details[2],re.I) != None:
                        self.apriori_search_x.append((details[0],details[1],details[2],details[3]))
                        column = 0
                        merge_x_y = ''
                        for det in details:
                            if column <= 1:
                                #det = "%.4f" % det
                                det = unicode(det)
                                testData = QtGui.QStandardItem(det)
                                self.model.setItem(count_job_num,column,testData)
                                column = column + 1
                            elif column == 2:
                                det = unicode(det,'utf-8')
                                merge_x_y = merge_x_y + det + '-->'
                                #print 'merge_x_y 11=',merge_x_y
                                column = column + 1
                            else:
                                det = unicode(det,'utf-8')
                                det = merge_x_y + det 
                                #print 'merge_x_y 22=',det
                                testData = QtGui.QStandardItem(det)
                                self.model.setItem(count_job_num,column - 1,testData)  #column 要 减去 1
                            #column = column + 1
                        #print 'column=',column
                        #print 'det =',det
                        count_job_num = count_job_num + 1
                
                self.tbl_anaysis_result.setModel(self.model)
                #设置tbl_job_details 列宽度
                self.tbl_anaysis_result.setColumnWidth(2,412)

         #############################
        #if cmp(apriori_y,'') != 0:
        #    print 'test'

        #从 强项 x 的搜索结果中再搜索后项 y
        self.tbl_anaysis_result.clearSpans()
        self.model.clear()
	self.model.setHorizontalHeaderLabels([u'支持度', u'置信度',u'具体内容 X-->Y '])
        apriori_y = unicode(self.ledit_the_latter.text())
        apriori_y = apriori_y.encode('utf-8')  #不然不支持中文搜索功能
        count_job_num = 0
        for details in self.apriori_search_x: 
            if re.search(apriori_y,details[3],re.I) != None:
                #self.apriori_search_x.append(details[0],details[1],details[2],details[3])
                column = 0
                merge_x_y = ''
                for det in details:
                    if column <= 1:
                        #det = "%.4f" % det
                        det = unicode(det)
                        testData = QtGui.QStandardItem(det)
                        self.model.setItem(count_job_num,column,testData)
                        column = column + 1
                    elif column == 2:
                        det = unicode(det,'utf-8')
                        merge_x_y = merge_x_y + det + '-->'
                        #print 'merge_x_y 11=',merge_x_y
                        column = column + 1
                    else:
                        det = unicode(det,'utf-8')
                        det = merge_x_y + det 
                        #print 'merge_x_y 22=',det
                        testData = QtGui.QStandardItem(det)
                        self.model.setItem(count_job_num,column - 1,testData)  #column 要 减去 1
                    #column = column + 1
                #print 'column=',column
                #print 'det =',det
                count_job_num = count_job_num + 1
	self.tbl_anaysis_result.setModel(self.model)
        #设置tbl_job_details 列宽度
        self.tbl_anaysis_result.setColumnWidth(2,412)


    @QtCore.pyqtSignature("")
    def on_btn_the_course_or_workplace_search_widget2_clicked(self):  
	analysisType = self.cmbx_analysis_type.currentIndex()
        jobType = self.cmbx_job_type_in_analysis.currentIndex()
        comText_analysisType = self.cmbx_analysis_type.itemText(analysisType)
        comText_analysisType = unicode(comText_analysisType)
        comText_analysisType = comText_analysisType.encode('utf-8')
        
        if cmp(comText_analysisType,'岗位地点热度') == 0:
            #ledit_course_or_workplace_widget2
            #self.popCourse = [] #保存课程热度的列表
            self.model.clear()
            self.tbl_anaysis_result.clearSpans()
            
            self.model.setHorizontalHeaderLabels([ u'地点',u'频率'])
            searchText = unicode(self.ledit_course_or_workplace_widget2.text())
            searchText = searchText.encode('utf-8')
            count_analysis_count = 0
            for details in self.popWorkplace: 
                print 'details[0]',details[0]
                print type(details[0])
                if re.search(searchText,details[0],re.I) != None:
                    print searchText
                    column = 0
                    for det in details:
                        if column <= 0:
                            det = unicode(det,'utf-8')
                            testData = QtGui.QStandardItem(det)
                            self.model.setItem(count_analysis_count,column,testData)
                            column = column + 1
                        else:
                            det = "%.4f" % det
                            det = unicode(det)
                            testData = QtGui.QStandardItem(det)
                            self.model.setItem(count_analysis_count,column ,testData)  #column 要 减去 1
                    count_analysis_count = count_analysis_count + 1

            #把相应的岗位总数，分析的结果总数，显示在相应的地方
            #self.ledit_position_count_widget2.setText(str(position_count))
            #self.ledit_analysis_result_count_widget2.setText(str(count_analysis_count))

            self.tbl_anaysis_result.setModel(self.model)
            self.tbl_anaysis_result.setColumnWidth(0,289)
            self.tbl_anaysis_result.setColumnWidth(1,289)
	
	elif cmp(comText_analysisType,'单门课程热度') == 0:
	    self.tbl_anaysis_result.clearSpans()
            self.model.clear()
            self.model.setHorizontalHeaderLabels([ u'课程',u'频率'])
            searchText = unicode(self.ledit_course_or_workplace_widget2.text())
            searchText = searchText.encode('utf-8')
            count_analysis_count = 0
            for details in self.popCourse: 
                print 'details[0]',details[0]
                print type(details[0])
                if re.search(searchText,details[0],re.I) != None:
                    print searchText
                    column = 0
                    for det in details:
                        if column <= 0:
                            det = unicode(det,'utf-8')
                            testData = QtGui.QStandardItem(det)
                            self.model.setItem(count_analysis_count,column,testData)
                            column = column + 1
                        else:
                            det = "%.4f" % det
                            det = unicode(det)
                            testData = QtGui.QStandardItem(det)
                            self.model.setItem(count_analysis_count,column ,testData)  #column 要 减去 1
                    count_analysis_count = count_analysis_count + 1

            #把相应的岗位总数，分析的结果总数，显示在相应的地方
            #self.ledit_position_count_widget2.setText(str(position_count))
            #self.ledit_analysis_result_count_widget2.setText(str(count_analysis_count))

            self.tbl_anaysis_result.setModel(self.model)
            self.tbl_anaysis_result.setColumnWidth(0,289)
            self.tbl_anaysis_result.setColumnWidth(1,289)
        else:
            #reply = QtGui.QMessageBox.question(self, 'Message',
            #   u"目前不是课程热度或者地点热度分析，不能使用该功能！", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            reply = QtGui.QMessageBox.question(self, 'Message',
               u"目前不是课程热度或者地点热度分析，不能使用该功能！", QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                pass
                #event.accept()
            else:
                pass
                #event.ignore()
                

    #修改关联分析的支持度和置信度
    @QtCore.pyqtSignature("")
    def on_btn_modify_support_and_confidence_clicked(self):
        supp = self.ledit_support.text()
        conf = self.ledit_confidence.text()
        supp = unicode(supp)
        conf = unicode(conf)
        supp = u'0.' + supp
        conf = u'0.' + conf
        try:
            supp = float(supp)
            conf = float(conf)
            print type(conf)
            print 'supp =',supp
            print 'conf =',conf
            self.associate_analysis_support = supp
            self.associate_analysis_confidence = conf
            reply = QtGui.QMessageBox.question(self, 'Message',
                u"修改成功，请重新查询", QtGui.QMessageBox.Yes)
        except ValueError:
            print 'error '
            reply = QtGui.QMessageBox.question(self, 'Message',
                u"请检查你的输入,有非数字字符", QtGui.QMessageBox.Yes)

    #导出数据到excel表中的按钮
    @QtCore.pyqtSignature("")
    def on_btn_export_excel_clicked(self):
        analysisType = self.cmbx_analysis_type.currentIndex()
        jobType = self.cmbx_job_type_in_analysis.currentIndex()
        comText_analysisType = self.cmbx_analysis_type.itemText(analysisType)
        comText_analysisType = unicode(comText_analysisType)
        
        comText_jobType = self.cmbx_job_type_in_analysis.itemText(jobType)
        comText_jobType = unicode(comText_jobType)
        comText_jobType = comText_jobType.encode('utf-8')

        if analysisType != 0 and jobType != 0:
            print comText_jobType
            if cmp(comText_analysisType,'单门课程热度') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_' + comText_jobType + '.xls' ,'excel(.xls)')
                    fileName = unicode(fileName)
                    self.export_execl_pop_courese(fileName)
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_Net.xls','excel(.xls)')
                    self.export_execl_pop_courese(fileName)
                else:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_NodeJs.xls','excel(.xls)')
                    self.export_execl_pop_courese(fileName)
                
            if cmp(comText_analysisType,'岗位地点热度') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_' + comText_jobType + '.xls' ,'excel(.xls)')
                    self.export_execl_pop_workplace(fileName)
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_Net.xls','excel(.xls)')
                    self.export_execl_pop_workplace(fileName)
                else:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_NodeJs.xls','excel(.xls)')
                    self.export_execl_pop_workplace(fileName)

            if cmp(comText_analysisType,'课程关联分析') == 0:
                if cmp(comText_jobType,'.Net') != 0 and cmp(comText_jobType,'Node.js') != 0:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_' + comText_jobType + '.xls' ,'excel(.xls)')
                    self.export_execl_apriori_course(fileName)
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_Net.xls','excel(.xls)')
                    self.export_execl_apriori_course(fileName)
                else:
                    fileName = QtGui.QFileDialog.getSaveFileName(self,'Export Excel',comText_analysisType + '_NodeJs.xls','excel(.xls)')
                    self.export_execl_apriori_course(fileName)

        else:
            reply = QtGui.QMessageBox.question(self, 'Message',
                u"还没有分析结果,请先分析", QtGui.QMessageBox.Yes)
            

    #开始爬取数据按钮事件 start_crawler_job_button 
    @QtCore.pyqtSignature("")
    def on_start_crawler_job_button_clicked(self):
	#mThreadPool.startCrawlerJob()
	self.processorThread.isFinished = True
	self.listWidget.addItem(u"启动爬虫程序...")
        if self.isFirstStartThread == True:	
            self.isFirstStartThread == False   #下次启动的时候不会在执行start()了
	    self.processorThread.start()

    #开始爬取数据按钮事件 stop_crawler_job_button 
    @QtCore.pyqtSignature("")
    def on_stop_crawler_job_button_clicked(self):
	self.processorThread.isFinished = False
        string = '停止爬数据。不过要爬完列表剩下的岗位!!!!!'
        s = unicode(string)
	self.processorThread.progressUpdated.emit(s)
	#self.listWidget.addItem(st)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dlg = Pyqtdemo()
    dlg.show()
    sys.exit(app.exec_())
