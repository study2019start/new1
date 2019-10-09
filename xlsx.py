from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook

def  print1(fd1):
    wb= load_workbook(fd1)
    sheets = wb['Sheet1']
    pr=[]
    pr1=[]
    rows=sheets.rows
    for row in rows:
        pr.append(row[2].value)
    
    print(pr)


if __name__=='__main__':
    print1(r'E:\黄浦金陵东路模板\金陵东路64号地块给评估公司清册.xlsx')



