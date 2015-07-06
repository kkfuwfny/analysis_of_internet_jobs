def test():
    fsh = file('savedHash.txt','r+')
    #while fsh.readline().strip('\n')!='55072010':
    #for i in range(3): 
  
    url = fsh.readline().strip('\n')
    while url!='':
 #self.container[int(self.fsh.readline())]=1
        print url
        url = fsh.readline().strip('\n')


test()    
