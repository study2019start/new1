import re


re1=r"[\u4e00-\u9fa5]+(\d{4})[\u4e00-\u9fa5]*"

def res(listt):
    for lis in listt:
        result=re.findall(re1,lis)
        if result:
            print(result[0])


if  __name__ == "__main__":
    lisd=["绿地外滩中心2018","绿地外滩2013中心","绿地2015"]
    res(lisd)