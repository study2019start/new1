import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import datetime
# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):

    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('pdf')
                 ]
    return file_list if file_list else []

# 合并同一目录下的所有PDF文件
def MergePDF(filepath,fs, outfile):

    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = getFileName(filepath)

    if pdf_fileName:
        for pdf_file in pdf_fileName:
            print("路径：%s"%pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            print("页数：%d"%pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        print("合并后的总页数:%d."%outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(fs, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")

# 主函数
if __name__ == '__main__': 
    time1 = time.time()
    file_dir =  os.path.join(os.getcwd(),"原始文件")
    print(file_dir)
    file_successfully= os.path.join(os.getcwd(),"完成") # 存放PDF的件夹
    if os.path.exists(file_dir):
        pass
    else:
        os.mkdir(file_dir)
    outfile = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))+".pdf"
    #str(time.strftime("%Y%m%d%H%M%S",time.localtime()))+ ".pdf"     # 输出的PDF文件的名称
    MergePDF(file_dir,file_successfully, outfile)
    time2 = time.time()
    print('总共耗时：%s s.' %(time2 - time1))