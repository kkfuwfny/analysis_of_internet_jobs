# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.Qt import *
from Ui_mainWindow import Ui_MainWindow
import jobDB
import apriori
import re
from push_button import *
from Login import login

apr = apriori.apriori()
db = jobDB.jobDB()

#列表内容区中显示
class CenterDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
    def paint(self, painter, option, index):
        painter.save()
        #painter.drawText(option.rect, Qt.AlignCenter, index.data(Qt.DisplayRole).toString())
	painter.drawText(option.rect, Qt.TextWordWrap | Qt.AlignHCenter, index.data(Qt.DisplayRole).toString())        
	painter.restore()

class Pyqtdemo(QtGui.QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor  
        """
	
        self.apriori_result = [] #保存关联分析的结果
        self.apriori_search_x = [] #保存关联分析之后，搜索前项 x 的保存结果
        self.apriori_search_y = [] #保存关联分析之后，搜索后项 y 的保存结果
        self.popCourse = [] #保存课程热度的列表
        self.popWorkplace = [] #保存岗位地点的热度列表
        self.analysis_type = '' #分析数据的类别 
        self.job_type = ''#要分析的工作类别 
        #self.admin_login
	self.model = QtGui.QStandardItemModel()	
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint) 
        self.setFixedSize(self.width(),self.height())
 	self.tool_button_background()        
	#self.load_data()
	self.tbl_job_details.setItemDelegate(CenterDelegate())       
        #self.tbl_job_details.resizeColumnToContents(8)
	self.center()    #窗口区中
        self.init_other_widget()
	self.label_3.setStyleSheet("color:white")        

	self.mouse_press = False
	self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        #隐藏第二个页面的一些关于搜索的部件，看情况显示

		
	#self.close_button.setPixmap(self.pixmap)
	
	self.initTitle()    ##########################################test######	


    def initTitle(self):
	#self.title_label =  QtGui.QLabel(self) 
	self.title_label.setText(u"analysis robot")
        #self.title_icon_label =  QtGui.QLabel(self)
        #self.close_button =  QtGui.QPushButton(self)

        title_pixmap = QPixmap ("./img/safe.ico")
        self.title_icon_label.setPixmap(title_pixmap)
        self.title_icon_label.setFixedSize(16, 16)
        self.title_icon_label.setScaledContents(True)

       
	#self.close_button = PushButton()
	#print 'btn =',self.close_button
	#print type(self.close_button)
	#self.close_button.loadPixmap("./img/sysButton/close.png")
	#self.close_button.setStyleSheet("background:transparent")
	#self.setFixedSize(self.btn_width, self.btn_height)
        self.title_label.setFixedHeight(30)
	'''
        self.title_layout = QtGui.QHBoxLayout()
        self.title_layout.addWidget(self.title_icon_label, 0, Qt.AlignVCenter)
        self.title_layout.addWidget(self.title_label, 0, Qt.AlignVCenter)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button, 0, Qt.AlignTop)
        self.title_layout.setSpacing(50)
        self.title_layout.setContentsMargins(10, 0, 5, 0)
	'''
        self.title_label.setStyleSheet("color:white")
        self.connect(self.close_button, SIGNAL("clicked()"), SLOT("close()"))
        #self.title_label.addStretch()
	#self.setLayout(self.title_layout) 

    

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
        self.painter2.drawRect(QRect(800, 60, self.width(), self.height() - 30));
        self.painter2.end()
        
        self.painter3 = QtGui.QPainter()
        self.painter3.begin(self)
        self.painter3.setPen(Qt.gray)
        self.painter3.drawPolyline(QtCore.QPointF(0, 30), QtCore.QPointF(0, self.height() - 1), QtCore.QPointF(self.width() - 1, self.height() - 1), QtCore.QPointF(self.width() - 1, 30))
	self.painter3.end()
	

  	
    def init_other_widget(self):
        # 1
        job_type_list = [u'------岗位类别-------',u'全部岗位',u'IOS',u'Android',u'Python',u'Java',u'C++',u'C#',u'.Net',u'测试',u'数据分析',u'数据库',u'架构师',u'UI',u'游戏',u'网页设计',u'网站',u'安全',u'运维',u'Perl',u'Ruby',u'Hadoop',u'Node.js',u'Php']
	for jt in job_type_list:
	    self.cmbx_job_type.addItem(jt)
        #self.connect(self.cmbx_job_type, QtCore.SIGNAL(self.currentIndexChanged(int)), this, QtCore.SLOT(self.comboBoxValueChanged())) 
	#self.connect(self.cmbx_job_type, QtCore.SIGNAL(self.cmbx_job_type.currentIndexChanged(int)), self.my_comboBox)
	
	self.connect(self.cmbx_job_type, QtCore.SIGNAL('currentIndexChanged(int)'), self.comboBoxValueChanged_job_details)

        # 2 
        search_item = [u'--------选择搜索项---------',u'公司名称',u'岗位名称',u'岗位地点']
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
        self.ledit_position_count_widget1.setText('')	
################################stackedWidgetPage2 函数区域22222222222222222222222222222222222222222222222222222
    

    #这个函数包含你太多的分析，可能会有点混乱
    def comboBoxValueChanged_job_type(self):
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
                    self.pop_course(fileName)            
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/workplace_result/" + "Net" + ".txt"
                    self.pop_course(fileName)            
                else:
                    fileName = "./save_analysis_result/workplace_result/" + "NodeJs" + ".txt"
                    self.pop_course(fileName)            

            if cmp(comText_analysisType,'课程关联分析') == 0:
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
        
        #print 'comnoBoxValueChanged_analysis'
        #comText = self.cmbx_job_type_in_analysis.itemText(self.cmbx_job_type_in_analysis.currentIndex())
        #print 'num=',self.cmbx_job_type_in_analysis.currentIndex()
        #if self.cmbx_job_type_in_analysis.currentIndex() == 1:
        #    print ' == 2'
        #    self.pop_course()
        #if self.cmbx_job_type_in_analysis.currentIndex() == 2:
        #    print ' == 2'
        #    self.pop_workplace()
        #if self.cmbx_job_type_in_analysis.currentIndex() > 3:

        #    self.apriori_course()
        #    qbyte = unicode(comText)
        #    print 'qbyte=',type(qbyte)
        #    print 'comText=',qbyte

    ######        
    def comboBoxValueChanged_analysis_type(self):
        #if self.cmbx_analysis_type.currentIndex() != 0 and self.cmbx_job_type_in_analysis.currentIndex() != 0: #如果没有岗位选择类别或者没有变化时
        analysisType = self.cmbx_analysis_type.currentIndex()
        jobType = self.cmbx_job_type_in_analysis.currentIndex()
        comText_analysisType = self.cmbx_analysis_type.itemText(analysisType)
        comText_analysisType = unicode(comText_analysisType)
        comText_analysisType = comText_analysisType.encode('utf-8')

        comText_jobType = self.cmbx_job_type_in_analysis.itemText(jobType)
        comText_jobType = unicode(comText_jobType)
        comText_jobType = comText_jobType.encode('utf-8')

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
                    self.pop_course(fileName)            
                elif cmp(comText_jobType,'.Net') == 0:
                    fileName = "./save_analysis_result/workplace_result/" + "Net" + ".txt"
                    self.pop_course(fileName)            
                else:
                    fileName = "./save_analysis_result/workplace_result/" + "NodeJs" + ".txt"
                    self.pop_course(fileName)            

            if cmp(comText_analysisType,'课程关联分析') == 0:
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
        self.apriori_result , position_count = apr.apriori_course(filename)
        #for ar in self.apriori_result:
        #    for a in ar:
        #        print 'a =',a,
        #    print '' 
        #print 'print Done.'
        self.model.setHorizontalHeaderLabels([u'支持度', u'置信度',u'具体内容 X-->Y '])
        count_analysis_count = 0  #不能删除，很关键，是插入第几列的
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
                    #column = column + 1
                #print 'column=',column
                #print 'det =',det
            count_analysis_count = count_analysis_count + 1

        #把相应的岗位总数，分析的结果总数，显示在相应的地方
        self.ledit_position_count_widget2.setText(str(position_count))
        self.ledit_analysis_result_count_widget2.setText(str(count_analysis_count))
        self.tbl_anaysis_result.setModel(self.model)
        self.tbl_anaysis_result.setColumnWidth(0,88)
        self.tbl_anaysis_result.setColumnWidth(1,88)
        self.tbl_anaysis_result.setColumnWidth(2,410)
        self.tbl_anaysis_result.resizeRowsToContents()

    #先确定要分析的类型有 关联分析，岗位地点分析，课程关联分析 
        

    #设置job_details_button的背景图片和样式
    def tool_button_background(self):
    	self.job_details_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/recovery.png")
	self.job_details_button.setIcon(QIcon(recovery_pixmap))
	self.job_details_button.setIconSize(recovery_pixmap.size())
	self.job_details_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	#修复hover样式
	self.job_details_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	#设置job_analysis_button 的背景图片和样式
	self.job_analysis_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/analysis.png")
	self.job_analysis_button.setIcon(QIcon(recovery_pixmap))
	self.job_analysis_button.setIconSize(recovery_pixmap.size())
	self.job_analysis_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	#修复hover样式
	self.job_analysis_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
	
    	
	#设置crawler_job_button 的背景图片和样式
	self.crawler_job_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/spider11.png")
	self.crawler_job_button.setIcon(QIcon(recovery_pixmap))
	self.crawler_job_button.setIconSize(recovery_pixmap.size())
	self.crawler_job_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	#修复hover样式
	self.crawler_job_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")
      

	#设置connect_us_button 的背景图片和样式
	self.connect_us_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/emil4.png")
	self.connect_us_button.setIcon(QIcon(recovery_pixmap))
	self.connect_us_button.setIconSize(recovery_pixmap.size())
	self.connect_us_button.setFixedSize(recovery_pixmap.width() + 50, recovery_pixmap.height() + 35)
	#修复hover样式
	self.connect_us_button.setStyleSheet("QToolButton{background:transparent}"
		"QToolButton:hover{border-radius:5px;border:1px solid rgb(210, 225, 230)}")

#self.close_button.loadPixmap("./img/sysButton/close.png")
	#设置close_button 的背景图片和样式
	self.close_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
	recovery_pixmap = QPixmap ("./img/toolButton/close.png")
	self.close_button.setIcon(QIcon(recovery_pixmap))
	self.close_button.setIconSize(recovery_pixmap.size())
	self.close_button.setFixedSize(recovery_pixmap.width() + 25, recovery_pixmap.height() + 15)
	
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
	self.connect(self.minimize_button, SIGNAL("showMin()"), self, SLOT("showMinimized()"))	


    #窗口居中 
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
	

    


    #第一个页面搜索按钮的函数 btn_search 
    @QtCore.pyqtSignature("")
    def on_btn_search_clicked(self):
        search_item_num = self.cmbx_search_item_widget1.currentIndex()
        search_item_contend = self.cmbx_search_item_widget1.itemText(search_item_num)
        search_item_contend = unicode(search_item_contend)
        search_item_contend = search_item_contend.encode('utf-8')
        if search_item_num == 0:
            reply = QtGui.QMessageBox.question(self, 'Message',
               u"请选择搜索项", QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        elif cmp(search_item_contend,'公司名称') == 0:
            condition = unicode(self.ledit_search.text())
            print 'condition =',condition
            print 'sic =',search_item_contend
            self.search_data_by_cmbx_search_item_widget1(search_item_contend,condition)
        elif cmp(search_item_contend,'岗位名称') == 0:
            condition = unicode(self.ledit_search.text())
            print 'condition =',condition
            print 'sic =',search_item_contend
            self.search_data_by_cmbx_search_item_widget1(search_item_contend,condition)
        else:
            condition = unicode(self.ledit_search.text())
            print 'condition =',condition
            print 'sic =',search_item_contend
            self.search_data_by_cmbx_search_item_widget1(search_item_contend,condition)


    
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

    #搜索关联规则前项 xbtn_the_course_search_widget2
    @QtCore.pyqtSignature("")
    def on_btn_the_course_search_widget2_clicked(self):  
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
        if cmp(apriori_y,'') != 0:
            print 'test'
        #从 强项 x 的搜索结果中再搜索后项 y
        self.tbl_anaysis_result.clearSpans()
        self.model.clear()
	self.model.setHorizontalHeaderLabels([u'支持度', u'置信度',u'具体内容 X-->Y '])
        apriori_y = unicode(self.ledit_the_latter.text())
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
    def on_btn_the_course_workplace_search_widget2_clicked(self):  
        #从 强项 x 的搜索结果中再搜索后项 y
        self.tbl_anaysis_result.clearSpans()
        self.model.clear()
	self.model.setHorizontalHeaderLabels([u'支持度', u'置信度',u'具体内容 X-->Y '])
        apriori_y = unicode(self.ledit_the_latter.text())
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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dlg = Pyqtdemo()
    dlg.show()
    sys.exit(app.exec_())
