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
if __name__ == "__main__":
    sp=[2,3,66,12,3,1,15,12,16,7,12,57]
    m=ac(r"F:\地价\test\test\conn\Database1.accdb")
    p=m.muselect({'dizhi':"青浦区华新镇蒋家巷路东侧44-02地块"},'bj_table')
    print(p)