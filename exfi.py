import os
import pyexiv2 as ev


global a
a = []
def bianli(path,find):
    global a
    if os.path.exists(path):
        list = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path1 = os.path.join(path,list[i])
            if os.path.isfile(path1):
                if path1.find(find)>0:
                    a.append(path1)
            else:
                bianli(path1,find)
def imgExif(path):
        try:
            # if self.DateTimeOriginal == "now":
            #     mytime = time.strftime('%Y:%m:%d %H:%M:%S',time.localtime(time.time()))
            # else:
            #     mytime = self.DateTimeOriginal
            exiv_image = ev.Image(path,encoding='gbk')
            f=exiv_image.read_exif()
            d={}
            for k,v in f.items():
                if k !="Exif.Photo.DateTimeOriginal":
                    d[k]=""
            exiv_image.modify_exif(d)
            
            #exiv_image["Exif.Image.Artist"] = ""
            #exiv_image["Exif.Photo.DateTimeOriginal"] = ""
            #exiv_image["Exif.Image.Software"] = "aa"
            # exiv_image["Exif.Image.Make"]=""
            # exiv_image["Exif.Image.Model"]=""
            # exiv_image["Exif.Image.ExposureTime"]=""
            # exiv_image["Exif.Image.FNumber"]=""
            # exiv_image["Exif.Image.ISO"]=""
            # exiv_image["Exif.Image.FocalLength"]=""
            # exiv_image["Exif.Image.ExposureMode"]=""
            # exiv_image["Exif.Image.WhiteBalance"]=""
            # exiv_image["Exif.Image.MaxApertureValue"]=""
            # exiv_image["Exif.Image.FocalLengthIn35mmForma"]=""
            # exiv_image["Exif.Image.MeteringMode"]=""
            # exiv_image["Exif.Image.Contrast"]=""
            # exiv_image["Exif.Image.Saturation"]=""
            # exiv_image["Exif.Image.ExifVersion"]=""

            #exiv_image.write()
            print(u'图片:',path,u'操作成功')
        except:
            print(u'图片:',path,u'操作失败')


if __name__ == "__main__":
    file_path=r"F:\地价\信衡\2\310000AS0064"
    bianli(file_path,"jpg")
    for asd in a:
        imgExif(asd)

     