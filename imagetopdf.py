from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image
import os
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfFileMerger


global a
a = []
def bianli(path,find):
    global a
    if os.path.exists(path):
        ii=0
        list1 = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list1)):
            path1 = os.path.join(path,list1[i])
            if os.path.isfile(path1):
                if path1.find(find)>0 and ii==0:
                    a.append(path)
                    ii=+1
            else:
                bianli(path1,find)

def image_topdf(file_list):
    lpl=[]
    print(file_list)
    for list12 in file_list:
        list1=os.listdir(list12)
        ii=1
        lp=[]
        for i in range(0,len(list1)):
            if list1[i].find("jpg")>0:
                if list1[i].find("季度")<0:
                    file1=os.path.join(list12,list1[i])
                    w,h=Image.open(file1).size
                    pdf_path=os.path.join(list12,"temp"+str(ii)+".pdf")
                    user = canvas.Canvas(pdf_path, pagesize=(w, h))
                    user.drawImage(file1, 0, 0, w, h)
                    user.showPage()
                    user.save()
                    ii=ii+1
                    lp.append(os.path.join(list12,pdf_path))
        lpl.append(lp)
    print(lpl)
    return lpl

def merge_pdf(list_pdf):
    
    if list_pdf:
        result_pdf=PdfFileMerger()
        file_path=list_pdf[0][:list_pdf[0].rfind("\\")]
        pdf_file=list_pdf[0][:list_pdf[0].rfind("\\")]
        final_pdf_file=pdf_file[pdf_file.rfind("\\")+1:]
        for pdf in list_pdf:
            with open(pdf,'rb') as fp:
                pdf_reader=PdfFileReader(fp)
                result_pdf.append(pdf_reader)
        result_pdf.write(os.path.join(file_path,final_pdf_file+".pdf"))

        result_pdf.close()
        for pdf in list_pdf:
            os.remove(pdf)
        
if __name__ == "__main__":
    file_p=r"F:\地价\任务\康晓磊"
    bianli(file_p,"jpg")
    
    lpp=image_topdf(a)
    for l in lpp:
        merge_pdf(l)