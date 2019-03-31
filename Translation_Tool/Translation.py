import tkinter as tk
import requests
import json
import js2py
import hashlib
import urllib.parse as up


class Google() :
    def __init__(self):
        self.js_code = '''
            function TL(a) {
                var k = "";
                var b = 406644;
                var b1 = 3293161072;
                var jd = ".";
                var $b = "+-a^+6";
                var Zb = "+-3^+b+-f";
                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var m = a.charCodeAt(g);
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = m >> 18 | 240,
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                    e[f++] = m >> 6 & 63 | 128),
                    e[f++] = m & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++) a += e[f],
                a = RL(a, $b);
                a = RL(a, Zb);
                a ^= b1 || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1E6;
                return a.toString() + jd + (a ^ b)
            };
            function RL(a, b) {
                var t = "a";
                var Yb = "+";
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2),
                    d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                    d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                    a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                }
                return a
            }
        '''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        self.url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl={}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={}&q={}'

    def isChinese(self, word):
        for w in word:
            if '\u4e00' <= w <= '\u9fa5':
                return True
        return False

    def getTk(self, word):
        evaljs = js2py.EvalJs()
        evaljs.execute(self.js_code)
        tk = evaljs.TL(word)
        return tk

    def translate(self, word):
        if len(word) > 4891:
            raise RuntimeError('The length of word should be less than 4891...')
        languages = ['zh-CN', 'en']
        if not self.isChinese(word):
            target_language = languages[0]
        else:
            target_language = languages[1]
        res = requests.get(self.url.format(target_language, self.getTk(word), word), headers = self.headers)
        return res.json()[0][0][0]


class Youdao() :

    def __init__(self) :
        self.url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'

    def getRequest(self, sentence) :
        _data = {
        'i': sentence,
        'from': 'AUTO',
        'to': 'Auto',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
        'typoResult': 'false',
        }

        response = requests.post(self.url, data=_data)
        if response.status_code == 200 :
            return response.text
        else :
            print("Something get error, please try again.")
            return None

    def getResult(self, response) :
        result_text = json.loads(response)
        #src = result_text['translateResult'][0][0]['src']
        tgt = result_text['translateResult'][0][0]['tgt']
        return tgt

    def translate(self, sentence) :
        Yapp = Youdao()
        response = Yapp.getRequest(sentence)
        result = Yapp.getResult(response)
        return result


class Baidu() :
    def __init__ (self):
        #self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate?'
        self.appid = '20170709000063735'
        self.key = 'EiXpUVJAu4mLYinEqgzN'
        self.salt = '1435660288'

    def isChinese(self, word):
        for w in word:
            if '\u4e00' <= w <= '\u9fa5':
                return True
        return False

    def translate(self, sentece) :
        if not self.isChinese(sentece) :
            tl = 'zh'
        else : tl = 'en'
        self.dic = {
        'q': sentece, 
        'from': 'auto',
        'to': tl,
        'appid': self.appid,
        'salt': self.salt,
        'sign': hashlib.md5((self.appid + sentece + self.salt + self.key).encode(encoding = 'utf-8')).hexdigest(),
        }
        # print(self.dic['sign'])
        r = requests.get(self.url + up.urlencode(self.dic))
        result = json.loads(r.text)['trans_result'][0]['dst']
        return result


Box_width = 470
Btn_width = 70
Btn_height = 30

class UI() :
    def __init__(self) :
        self.window = tk.Tk()
        self.window.title("Tranlation Tool")
        self.window.geometry('600x500')

        # submit button
        self.GG_btn = tk.Button(self.window, text = "谷歌翻译", command = lambda: self.submit(platform = "google"))
        self.GG_btn.place(x = Box_width + 30, y = 20, width = Btn_width, height = Btn_height)

        self.YD_btn = tk.Button(self.window, text = "有道翻译",  command = lambda: self.submit(platform = "youdao"))
        self.YD_btn.place(x = Box_width + 30, y = 70, width = Btn_width, height = Btn_height)

        self.BD_btn = tk.Button(self.window, text = "百度翻译", command = lambda: self.submit(platform = "baidu"))
        self.BD_btn.place(x = Box_width + 30, y = 120, width = Btn_width, height = Btn_height)

        # input box
        self.entry = tk.Entry(self.window)
        self.entry.place(x = 10, y = 20, width = Box_width, height = 30)
        self.entry.bind('<Key-Return>', self.submit)

        # the title of result
        self.title_text = tk.Label(self.window, text = "翻译结果：")
        self.title_text.place(x = 10, y = 60)

        # translation result
        self.result_text = tk.Text(self.window, background = "#FAFAFA")
        self.result_text.place(x = 10, y = 90, width = Box_width, height = 260)

        # translators
        self.YD_translator = Youdao()
        self.GG_translator = Google()
        self.BD_translator = Baidu()

    def submit(self, event = None, platform = 'google') :

        context = self.entry.get()
        
        if platform == 'google' :
            result = self.GG_translator.translate(context)
        elif platform == 'youdao' :
            result = self.YD_translator.translate(context)
        elif platform == 'baidu' :
            result = self.BD_translator.translate(context)
        else :
            raise RuntimeError('Platform only is only Google, Youdao or Baidu.')
        # translators
        # result = self.GG_translator.translate(context)
        # result = self.YD_translator.translate(context)
        # result = self.BD_translator.translate(context)
        # result = "Nothing"

        # 文本框中实际是从1.0 开始的,(0.n 来说是比文本内容还要上一行，超过文本框或者文本框开头)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def run(self) :
        self.window.mainloop()


if __name__ == '__main__':
    win = UI()
    win.run()
