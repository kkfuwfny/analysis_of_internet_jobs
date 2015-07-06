#-*- coding:utf-8 -*-
#这个程序把课程导入数据库中，可以去重
from bloomFilter import bloomfilter
import jobDB 


if __name__ == '__main__':
    bf = bloomfilter.BloomFilter('./bloomFilter/coursesHash.txt',True)
    jDB = jobDB.jobDB()
    jDB.create_courses()  #建立表courses，如果存在会删除原来的表格
    course_file = open('./courses/courses.txt','r')
    
    course = course_file.readline().strip('\n')
    while course != '':
        if bf.isContaions(course) == False:  
            bf.insert(course)
            print course
            jDB.insertCourse(course)
        else:
            print '\n---------------------\n' + course + ' has exists.'
            print '---------------------\n'
        course = course_file.readline().strip('\n')


