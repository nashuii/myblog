from bs4 import BeautifulSoup
from urllib import request


class News():
    html = request.urlopen('http://tech.ifeng.com')
    soup = BeautifulSoup(html,'html.parser')
    hotnews = soup.find_all('div',class_="hotNews")
    title,href = [],[]
    for i in hotnews:
        title.append(i.find('a').string)
        href.append(i.find('a').get('href'))

    @classmethod
    def result(self):  # zip对象是迭代器，必须在每次调用时重新生成，不然页面刷新后没有内容
        return zip(self.title,self.href)



