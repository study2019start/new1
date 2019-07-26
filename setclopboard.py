import win32clipboard as wc
import win32con


class Sc(object):

    def __init__(self):
        i=0


    def set_text(self,strs):
	    """ 写入 """
	    wc.OpenClipboard()
	    wc.EmptyClipboard()
	    wc.SetClipboardData(win32con.CF_UNICODETEXT,strs)
	    wc.CloseClipboard()