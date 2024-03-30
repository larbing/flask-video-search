


class PageMaster(object):

    def __init__(self,resutls,pageN=0,pageSize=10,pagecount=0,total=0) -> None:
        self.resutls   = resutls
        self.pageN     = pageN
        self.pageSize  = pageSize
        self.pagecount = pagecount
        self.total     = total 

    def get_pagination(self):
        num = max(self.pageN,1)
        start  = 1  if num <= 10  else num -5
        end    = 10 if num <= 10  else min( num+10 // 2 , self.pagecount)        
        return range(start,end+1)
    
    def get_next_page(self):
        return min(self.pageN + 1,self.pagecount)
    
    def get_up_page(self):
        return max(self.pageN - 1,1)
    
    def is_current_page(self,number):
        return self.pageN == number

    def __iter__(self):
        return self.resutls.__iter__()
    
    def __next__(self):
        return self.resutls.__next__()