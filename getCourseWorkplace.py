#coding:utf-8
#getCourseWorkplace.py

import jobDB
import time
db = jobDB.jobDB()

class getCourseWorkplace():
    
    # 从数据库中的岗位的岗位需求中获取课程
    def get_workplace_to_file(self):
        condition_list =  ['全部岗位','IOS','Android','Python','Java','C++','C#','.Net','测试','数据分析','数据库','架构师','人机交互','UI','游戏','网页设计','网站','安全','运维','Perl','Ruby','Hadoop','Node.Js','Php']
        file_former = './save_analysis_result/workplace_result/'

        for condition in condition_list:
            print 'condition',condition
            if cmp(condition,'.Net') == 0:
                db.get_job_workplace_by_condition('.Net' , file_former + 'Net.txt')
            elif cmp(condition,'Node.Js') == 0:
                db.get_job_workplace_by_condition('Node.Js' , file_former + 'NodeJs.txt')
            elif cmp(condition,'全部岗位') == 0:
                db.get_job_workplace_by_condition('' , file_former + '全部岗位.txt')
            else:
                db.get_job_workplace_by_condition(condition , file_former + condition + '.txt')

    def get_course_to_file(self):
        condition_list =  ['IOS','Android','Python','Java','C++','C#','.Net','测试','数据分析','数据库','架构师','人机交互','UI','游戏','网页设计','网站','安全','运维','Perl','Ruby','Hadoop','Node.Js','Php','全部岗位']
        file_former = './save_analysis_result/apriori_course_result/'

        for condition in condition_list:
            print 'condition',condition
            if cmp(condition,'.Net') == 0:
                db.get_job_course_by_position('.Net' , file_former + 'Net.txt')
            elif cmp(condition,'Node.Js') == 0:
                db.get_job_course_by_position('Node.js' , file_former + 'NodeJs.txt')
            elif cmp(condition,'全部岗位') == 0:
                db.get_job_course_by_position('' , file_former + '全部岗位.txt')
            else:
                db.get_job_course_by_position(condition , file_former + condition + '.txt')
        
    #def get_single_courset_frequency_to_file(self):
    #    return
            



if __name__ == '__main__':
    startTime = time.clock()
    getCW = getCourseWorkplace()
    getCW.get_workplace_to_file()
    endTime = time.clock()
    #getCW.get_course_to_file()
    #print "runing time is : %0.3f second" % (endTime - startTime)
    print "runing time is : %0.3f second" %  startTime
    print 'Done'




