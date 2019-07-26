from aip import AipOcr


class BaiduApi(object):

    def __init__(self):
        APP_ID = '16340052'
        API_KEY = '2OywNvj7YeyyqCFHG8QNNZt3'
        SECRET_KEY = 'pwerzEzc44uGB4s83v4oW8w1VU12osN9'
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


    def picture(self, filepath):
        image = self.getPicture1(filepath)
        text = self.client.basicGeneral(image)
        alltext = ""
        for item in text['words_result']:
            alltext = alltext+''.join(item.get('words', ''))+'\n'
        return alltext



    def getPicture1(cls, filepath):
        with open(filepath, 'rb') as f:
            return f.read()
