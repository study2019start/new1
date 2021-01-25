import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import datetime
import fitz
from cv2 import cv2 
# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):

    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('pdf')
                 ]
    return file_list if file_list else []

def PdftoImage(file_path):
    if os.path.exists(file_path):
        file_path_1=file_path[:file_path.rfind(".")]
        pdf=fitz.open(file_path)
        if pdf.pageCount>2:
            png_name=file_path_1+".png"
            png_name2=file_path_1+"_jie.png"
            if os.path.exists(png_name):
                os.remove(png_name)
            if os.path.exists(png_name2):
                os.remove(png_name2)
            rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
            zoom_y = 1.33333333
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            png=pdf[2].getPixmap(matrix=mat, alpha=False)
            png.writePNG(png_name)
            pngg=cv2.imread(png_name)
            kuan=pngg.shape[0]
            chang=int(pngg.shape[1]*0.3)
            print(pngg.shape)
            cropped=pngg[0:chang,0:kuan]
            cv2.imwrite(png_name2,cropped)
            return png_name,png_name2



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
    f=os.path.join(os.getcwd(),"G2019-02270.pdf")
    print(file_dir)
    if os.path.exists(file_dir):
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
    pn_1,pn_2=PdftoImage(f)
    