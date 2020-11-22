from access import access_model as ac


class A:

    def __init__(self, name, age):
        self.name =name
        self.age = age

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            obj = object.__new__(cls)
            cls.__instance = obj
        return cls.__instance
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
       
        mappings = dict()
        fields = []
        primaryKey = None
        print(cls.__module__)
        for k, v in attrs.items():
            if isinstance(v, Field):
               
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        pass
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
           pass
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        print(fields)
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
       
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                
                setattr(self, key, value)
        return value

class mm(Model):
    ip=IntegerField("mmip",True,0)
    ip2=IntegerField("mmip2",False,0)
    fp=3
    @classmethod
    def show(cls):
        print(cls.__dict__)


def gb(lis):

    le=len(lis)
    if le <=1:
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
    a=mm(ip=33,ip2=22)
     
    print(a.getValue("ip"))
    a.show()
    # ret1 = A("小明", 20)
    # ret2 = A("小花", 28)
    # ret3 = A("小白", 34)
    # print(ret1.__dict__)
    # sp=[2,1]
    # st1(i=5,iii=33)
    # a=1
    # b=a
    # a=b+1
    # print(a,b)
    # sp1=spp(7)
    # sp2=spp(77)
    # print(sp1.another_list)
    # print(sp1.some_list)
    # print(SomeClass.another_list)
    # print(sp2.another_list)
    # spp.spp2=17
    # sp1.spp2=[2,3,6]
    # print(sp1.spp2)
    # print(sp2.spp2)
    # print(spp.spp2)
    #m=ac(r"F:\地价\test\test\conn\Database1.accdb")
    #p=m.muselect({'dizhi':"青浦区华新镇蒋家巷路东侧44-02地块"},'bj_table')
    #