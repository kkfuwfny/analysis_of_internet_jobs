#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BitVector
import cmath
import random
import time
class HashType():  
    
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed
    
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap-1) & ret

class BloomFilter():
    '''
    exists 函数是用于检测某个值是否已经被标记的函数，应传入想要检测的值'''

    def __init__(self, amount = 1 << 25):
        '''amount是储存空间的个数(bits)'''
        self.container_size = amount
	self.count=0
        self.hash_amount = 7 #哈希函数的个数
        self.container = BitVector.BitVector(size = int(self.container_size)) #分配内存
        self.hash_seeds = [5, 7, 11, 13, 31, 37, 61]
        #import saved hash number
        self.fsh = open('./bloomFilter/savedHash.txt','r')
	
	self.savedHash=self.fsh.readline().strip('\n')
        while self.savedHash!='':
            self.container[int(self.savedHash)]=1
            #print int(self.savedHash)
	    self.savedHash=self.fsh.readline().strip('\n')
	self.fsh.close()
        
	self.hash = []
        for i in range(int(self.hash_amount)): #生成哈希函数
            self.hash.append(HashType(self.container_size, self.hash_seeds[i]))
        return 

    def exists(self, value):
        '''存在返回真，否则返回假'''
        if value == None:
            return False 
        for func in self.hash :
            if self.container[func.hash(str(value))] == 0 :
                return False
            return True

    def mark_value(self, value):
        '''value是要标记的元素'''
	self.fsh = open('./bloomFilter/savedHash.txt','a')
        for func in self.hash :
            self.container[func.hash(str(value))] = 1
	    self.fsh.write(str(func.hash(str(value)))+'\n')
           # print func.hash(str(value))
	    #print self.count
	    #self.count+=1
	self.fsh.close()
        return
    def __del__(self):
       self.fsh.close()
"""
def main():
    f=open('urls.txt','r+')
    bloomfilter = BloomFilter()
    while True:
        #url = raw_input()
        url = f.readline().strip('\n')
        #print url
        if url=='exit':
	    break
        if bloomfilter.exists(url) == False:
            bloomfilter.mark_value(url)
        else:
            print 'url :%s has exist' % url 
    print 'end!' 
main()
"""
