from access import access_model as ac

def gb(lis):

    le=len(lis)
    if le <=2:
        return lis
    f=int(le/2)
    a1=gb(lis[:f])
    a2=gb(lis[f:])
    print(a1)
    print(a2)
    result= merge(a1)+merge(a2)
    return merge(result)
def merge(ls):
    f=len(ls)
    mid=int(f/2)
    i=0
    j=mid
    b=[]
    while i< mid and j<f:
        if ls[i]>ls[j]:
            b.append(ls[j])
            j=j+1
        else:
            b.append(ls[i])
            i=i+1
    while i<mid:
        b.append(ls[i])
        i=i+1
    while j<f:
        b.append(ls[j])
        j=j+1
     
    return b

class SomeClass(object):
    some_var = 15
    some_list = [3]
    another_list = [5]
    def __init__(self,x):
        self.some_var = x + 1
        self.some_list = self.some_list + [x]
        self.another_list += [x]


class spp(SomeClass):
    some_var1 = 15
    spp2=16
    some_list = [5]
    #another_list = [6]
    def __init__(self,x):
        super(spp,self).__init__(x)
        self.some_var1 =x
        

def st1(i=2,ii=4,iii=6):
    print(i,"\n",ii,"\n",iii)

if __name__ == "__main__":
    sp=[2,3,66,12,3,1,15,12,16,7,12,57]
    st1(i=5,iii=33)
    a=1
    b=a
    a=b+1
    print(a,b)
    sp1=spp(7)
    sp2=spp(77)
    print(sp1.another_list)
    print(sp1.some_list)
    print(SomeClass.another_list)
    print(sp2.another_list)
    spp.spp2=17
    sp1.spp2=[2,3,6]
    print(sp1.spp2)
    print(sp2.spp2)
    print(spp.spp2)
    #m=ac(r"F:\地价\test\test\conn\Database1.accdb")
    #p=m.muselect({'dizhi':"青浦区华新镇蒋家巷路东侧44-02地块"},'bj_table')
    #