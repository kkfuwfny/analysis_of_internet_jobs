# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/lvchuan/python/main_widget.ui'
#
# Created: Tue Jul  7 09:56:10 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1019, 600)
        self.stackedWidget = QtGui.QStackedWidget(Form)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setGeometry(QtCore.QRect(-20, 10, 911, 601))
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.stackedWidgetPage1 = QtGui.QWidget()
        self.stackedWidgetPage1.setObjectName(_fromUtf8("stackedWidgetPage1"))
        self.cmbx_job_type = QtGui.QComboBox(self.stackedWidgetPage1)
        self.cmbx_job_type.setGeometry(QtCore.QRect(750, 10, 131, 31))
        self.cmbx_job_type.setObjectName(_fromUtf8("cmbx_job_type"))
        self.ledit_search = QtGui.QLineEdit(self.stackedWidgetPage1)
        self.ledit_search.setGeometry(QtCore.QRect(500, 10, 131, 31))
        self.ledit_search.setObjectName(_fromUtf8("ledit_search"))
        self.cmbx_search_item_widget1 = QtGui.QComboBox(self.stackedWidgetPage1)
        self.cmbx_search_item_widget1.setGeometry(QtCore.QRect(330, 10, 141, 31))
        self.cmbx_search_item_widget1.setObjectName(_fromUtf8("cmbx_search_item_widget1"))
        self.label_job_type_num = QtGui.QLabel(self.stackedWidgetPage1)
        self.label_job_type_num.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.label_job_type_num.setObjectName(_fromUtf8("label_job_type_num"))
        self.ledit_position_count_widget1 = QtGui.QLineEdit(self.stackedWidgetPage1)
        self.ledit_position_count_widget1.setGeometry(QtCore.QRect(190, 10, 121, 31))
        self.ledit_position_count_widget1.setObjectName(_fromUtf8("ledit_position_count_widget1"))
        self.tbl_job_details = QtGui.QTableView(self.stackedWidgetPage1)
        self.tbl_job_details.setEnabled(True)
        self.tbl_job_details.setGeometry(QtCore.QRect(10, 50, 871, 521))
        self.tbl_job_details.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.tbl_job_details.setObjectName(_fromUtf8("tbl_job_details"))
        self.tool_btn_search = QtGui.QToolButton(self.stackedWidgetPage1)
        self.tool_btn_search.setGeometry(QtCore.QRect(650, 10, 81, 31))
        self.tool_btn_search.setText(_fromUtf8(""))
        self.tool_btn_search.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.tool_btn_search.setObjectName(_fromUtf8("tool_btn_search"))
        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.stackedWidgetPage2 = QtGui.QWidget()
        self.stackedWidgetPage2.setObjectName(_fromUtf8("stackedWidgetPage2"))
        self.cmbx_analysis_type = QtGui.QComboBox(self.stackedWidgetPage2)
        self.cmbx_analysis_type.setGeometry(QtCore.QRect(640, 10, 131, 27))
        self.cmbx_analysis_type.setObjectName(_fromUtf8("cmbx_analysis_type"))
        self.tbl_anaysis_result = QtGui.QTableView(self.stackedWidgetPage2)
        self.tbl_anaysis_result.setGeometry(QtCore.QRect(10, 50, 621, 521))
        self.tbl_anaysis_result.setObjectName(_fromUtf8("tbl_anaysis_result"))
        self.ledit_the_former = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_the_former.setGeometry(QtCore.QRect(730, 100, 161, 27))
        self.ledit_the_former.setObjectName(_fromUtf8("ledit_the_former"))
        self.btn_the_course_or_workplace_search_widget2 = QtGui.QPushButton(self.stackedWidgetPage2)
        self.btn_the_course_or_workplace_search_widget2.setGeometry(QtCore.QRect(750, 310, 111, 27))
        self.btn_the_course_or_workplace_search_widget2.setObjectName(_fromUtf8("btn_the_course_or_workplace_search_widget2"))
        self.ledit_the_latter = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_the_latter.setGeometry(QtCore.QRect(730, 150, 161, 27))
        self.ledit_the_latter.setObjectName(_fromUtf8("ledit_the_latter"))
        self.lbl_search_former = QtGui.QLabel(self.stackedWidgetPage2)
        self.lbl_search_former.setGeometry(QtCore.QRect(650, 96, 71, 31))
        self.lbl_search_former.setObjectName(_fromUtf8("lbl_search_former"))
        self.lbl_search_latter = QtGui.QLabel(self.stackedWidgetPage2)
        self.lbl_search_latter.setGeometry(QtCore.QRect(650, 150, 71, 31))
        self.lbl_search_latter.setObjectName(_fromUtf8("lbl_search_latter"))
        self.cmbx_job_type_in_analysis = QtGui.QComboBox(self.stackedWidgetPage2)
        self.cmbx_job_type_in_analysis.setGeometry(QtCore.QRect(780, 10, 131, 27))
        self.cmbx_job_type_in_analysis.setObjectName(_fromUtf8("cmbx_job_type_in_analysis"))
        self.label_job_type_num_widget2 = QtGui.QLabel(self.stackedWidgetPage2)
        self.label_job_type_num_widget2.setGeometry(QtCore.QRect(140, 10, 71, 31))
        self.label_job_type_num_widget2.setObjectName(_fromUtf8("label_job_type_num_widget2"))
        self.ledit_position_count_widget2 = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_position_count_widget2.setGeometry(QtCore.QRect(220, 10, 131, 31))
        self.ledit_position_count_widget2.setObjectName(_fromUtf8("ledit_position_count_widget2"))
        self.label_job_analysis_num_widget2 = QtGui.QLabel(self.stackedWidgetPage2)
        self.label_job_analysis_num_widget2.setGeometry(QtCore.QRect(380, 10, 71, 31))
        self.label_job_analysis_num_widget2.setObjectName(_fromUtf8("label_job_analysis_num_widget2"))
        self.ledit_analysis_result_count_widget2 = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_analysis_result_count_widget2.setGeometry(QtCore.QRect(470, 10, 131, 31))
        self.ledit_analysis_result_count_widget2.setObjectName(_fromUtf8("ledit_analysis_result_count_widget2"))
        self.lbl_search_course_or_workplace_widget2 = QtGui.QLabel(self.stackedWidgetPage2)
        self.lbl_search_course_or_workplace_widget2.setGeometry(QtCore.QRect(650, 260, 71, 31))
        self.lbl_search_course_or_workplace_widget2.setObjectName(_fromUtf8("lbl_search_course_or_workplace_widget2"))
        self.ledit_course_or_workplace_widget2 = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_course_or_workplace_widget2.setGeometry(QtCore.QRect(730, 260, 161, 27))
        self.ledit_course_or_workplace_widget2.setObjectName(_fromUtf8("ledit_course_or_workplace_widget2"))
        self.btn_the_course_search_widget2 = QtGui.QPushButton(self.stackedWidgetPage2)
        self.btn_the_course_search_widget2.setGeometry(QtCore.QRect(750, 200, 111, 27))
        self.btn_the_course_search_widget2.setObjectName(_fromUtf8("btn_the_course_search_widget2"))
        self.cmbx_support = QtGui.QComboBox(self.stackedWidgetPage2)
        self.cmbx_support.setGeometry(QtCore.QRect(710, 380, 81, 27))
        self.cmbx_support.setObjectName(_fromUtf8("cmbx_support"))
        self.label_support = QtGui.QLabel(self.stackedWidgetPage2)
        self.label_support.setGeometry(QtCore.QRect(650, 380, 66, 17))
        self.label_support.setObjectName(_fromUtf8("label_support"))
        self.label_confidence = QtGui.QLabel(self.stackedWidgetPage2)
        self.label_confidence.setGeometry(QtCore.QRect(650, 430, 66, 17))
        self.label_confidence.setObjectName(_fromUtf8("label_confidence"))
        self.cmbx_confidence = QtGui.QComboBox(self.stackedWidgetPage2)
        self.cmbx_confidence.setGeometry(QtCore.QRect(710, 430, 81, 27))
        self.cmbx_confidence.setObjectName(_fromUtf8("cmbx_confidence"))
        self.ledit_support = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_support.setGeometry(QtCore.QRect(790, 380, 111, 27))
        self.ledit_support.setObjectName(_fromUtf8("ledit_support"))
        self.ledit_confidence = QtGui.QLineEdit(self.stackedWidgetPage2)
        self.ledit_confidence.setGeometry(QtCore.QRect(790, 430, 111, 27))
        self.ledit_confidence.setObjectName(_fromUtf8("ledit_confidence"))
        self.btn_modify_support_and_confidence = QtGui.QPushButton(self.stackedWidgetPage2)
        self.btn_modify_support_and_confidence.setGeometry(QtCore.QRect(750, 480, 111, 27))
        self.btn_modify_support_and_confidence.setObjectName(_fromUtf8("btn_modify_support_and_confidence"))
        self.stackedWidget.addWidget(self.stackedWidgetPage2)
        self.stackedWidgetPage3 = QtGui.QWidget()
        self.stackedWidgetPage3.setObjectName(_fromUtf8("stackedWidgetPage3"))
        self.stop_crawler_job_button = QtGui.QToolButton(self.stackedWidgetPage3)
        self.stop_crawler_job_button.setGeometry(QtCore.QRect(800, 320, 91, 71))
        self.stop_crawler_job_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.stop_crawler_job_button.setObjectName(_fromUtf8("stop_crawler_job_button"))
        self.start_crawler_job_button = QtGui.QToolButton(self.stackedWidgetPage3)
        self.start_crawler_job_button.setGeometry(QtCore.QRect(800, 190, 91, 71))
        self.start_crawler_job_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.start_crawler_job_button.setObjectName(_fromUtf8("start_crawler_job_button"))
        self.listWidget = QtGui.QListWidget(self.stackedWidgetPage3)
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 761, 481))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.stackedWidget.addWidget(self.stackedWidgetPage3)
        self.stackedWidgetPage4 = QtGui.QWidget()
        self.stackedWidgetPage4.setObjectName(_fromUtf8("stackedWidgetPage4"))
        self.textBrowser = QtGui.QTextBrowser(self.stackedWidgetPage4)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(240, 60, 471, 511))
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.stackedWidget.addWidget(self.stackedWidgetPage4)
        self.label_logo = QtGui.QLabel(Form)
        self.label_logo.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.label_logo.setObjectName(_fromUtf8("label_logo"))
        self.title_label = QtGui.QLabel(Form)
        self.title_label.setGeometry(QtCore.QRect(60, 0, 221, 31))
        self.title_label.setObjectName(_fromUtf8("title_label"))
        self.minimize_button = QtGui.QToolButton(Form)
        self.minimize_button.setGeometry(QtCore.QRect(940, 0, 31, 41))
        self.minimize_button.setText(_fromUtf8(""))
        self.minimize_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.minimize_button.setObjectName(_fromUtf8("minimize_button"))
        self.close_button = QtGui.QToolButton(Form)
        self.close_button.setGeometry(QtCore.QRect(970, 0, 41, 41))
        self.close_button.setText(_fromUtf8(""))
        self.close_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.close_button.setObjectName(_fromUtf8("close_button"))
        self.crawler_job_button = QtGui.QToolButton(Form)
        self.crawler_job_button.setGeometry(QtCore.QRect(920, 340, 91, 71))
        self.crawler_job_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.crawler_job_button.setObjectName(_fromUtf8("crawler_job_button"))
        self.job_analysis_button = QtGui.QToolButton(Form)
        self.job_analysis_button.setGeometry(QtCore.QRect(920, 220, 91, 71))
        self.job_analysis_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.job_analysis_button.setObjectName(_fromUtf8("job_analysis_button"))
        self.connect_us_button = QtGui.QToolButton(Form)
        self.connect_us_button.setGeometry(QtCore.QRect(920, 460, 91, 71))
        self.connect_us_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.connect_us_button.setObjectName(_fromUtf8("connect_us_button"))
        self.job_details_button = QtGui.QToolButton(Form)
        self.job_details_button.setGeometry(QtCore.QRect(920, 100, 91, 71))
        self.job_details_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.job_details_button.setObjectName(_fromUtf8("job_details_button"))
        self.label_connect_network = QtGui.QLabel(Form)
        self.label_connect_network.setGeometry(QtCore.QRect(690, 0, 151, 21))
        self.label_connect_network.setText(_fromUtf8(""))
        self.label_connect_network.setObjectName(_fromUtf8("label_connect_network"))

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_job_type_num.setText(_translate("Form", "岗位数量：", None))
        self.btn_the_course_or_workplace_search_widget2.setText(_translate("Form", "搜索课程/地点", None))
        self.lbl_search_former.setText(_translate("Form", "搜索前项", None))
        self.lbl_search_latter.setText(_translate("Form", "搜索后项", None))
        self.label_job_type_num_widget2.setText(_translate("Form", "岗位数量：", None))
        self.label_job_analysis_num_widget2.setText(_translate("Form", "结果数量：", None))
        self.lbl_search_course_or_workplace_widget2.setText(_translate("Form", "课程/地点", None))
        self.btn_the_course_search_widget2.setText(_translate("Form", "搜    索", None))
        self.label_support.setText(_translate("Form", "支持度", None))
        self.label_confidence.setText(_translate("Form", "置信度", None))
        self.btn_modify_support_and_confidence.setText(_translate("Form", "搜索课程/地点", None))
        self.stop_crawler_job_button.setText(_translate("Form", "停止爬取", None))
        self.start_crawler_job_button.setText(_translate("Form", "开始爬数据", None))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">有问题可以反馈给开开发者。开发者邮箱airlvchuan@sina.com。</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">反馈问题的时候，请务必详细一点，可以把截图也发过来。谢谢您的反馈，感激不尽。</p></body></html>", None))
        self.label_logo.setText(_translate("Form", "logo", None))
        self.title_label.setText(_translate("Form", "标题名字", None))
        self.crawler_job_button.setText(_translate("Form", "爬取数据", None))
        self.job_analysis_button.setText(_translate("Form", "岗位分析", None))
        self.connect_us_button.setText(_translate("Form", "联系我们", None))
        self.job_details_button.setText(_translate("Form", "岗位详情", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

