#_*_coding:utf_8_
import BitVector
import os
import sys

class SimpleHash():  
    
    def __init__(self, capability, seed):
        self.capability = capability
        self.seed = seed

    #传入的value即为url值，ord(value[i])表示第i位字符的ascii码值
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret + ord(value[i])
        #最终产生的随机数是二进制向量最大下标与随机数的按位与结果
        return (self.capability-1) & ret    

class BloomFilter():
    
    def __init__(self, BIT_SIZE=1<<25):
        self.BIT_SIZE = 1 << 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        #建立一个大小为1<<25=33554432位的二进制向量，分配内存
	self.bitset = BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc = []        
	self.fsh = open('./bloomFilter/savedHash.txt','r+')     
	self.savedHash=self.fsh.readline().strip('\n')
        while self.savedHash!='':
            self.bitset[int(self.savedHash)]=1
            #print int(self.savedHash)

	    self.savedHash=self.fsh.readline().strip('\n')   
    	self.fsh.close()
        #利用8个素数初始化8个随机数生成器
        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))
        
    def insert(self, value):
	self.fsh = open('./bloomFilter/savedHash.txt','a')
        for f in self.hashFunc:
	    self.fsh.write(str(f.hash(str(value)))+'\n') 	
            loc = f.hash(value)
            self.bitset[loc] = 1
	self.fsh.close()
    def isContaions(self, value):
        if value == None:
            return False
        ret = True
        for f in self.hashFunc:
            loc = f.hash(value)
            #用同样的随机数产生方法对比相应位的二进制值，只要发现有一个不同即返回结果为假
            ret = ret & self.bitset[loc]
            if ret==False:
                return ret
        #只有当8个二进制位都相等时才返回真
        return ret


