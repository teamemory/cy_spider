#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import lxml
import requests
import xlsxwriter


class Spider():
    # 初始化参数
    def __init__(self, urlList):
        self.urlList = urlList
        self.num = 0
        self.row = 0
        self.col = 0
        self.wookbook = ''
        self.wooksheet = ''
        self.id = 0

    # 下载
    def downLoad(self, add_url):
        print('开始下载html')
        res = requests.get(add_url)
        res.encoding = 'gb2312'
        html = res.text
        # print(html)
        self.analy(html)

    # 解析html
    def analy(self, html):
        print('开始解析html')
        soup = BeautifulSoup(html, 'html5lib')
        # 图片路径集合
        img_list = soup.select('.cyimg_list a img')
        # print(img_list)
        # 成语标题集合
        title_list = soup.select('.cyimg_list li a p')
        print(title_list)
        # 保存所有数据
        self.save_data(img_list,title_list)
        
    #保存图片和文字
    def save_data(self,img_list,title_list):
        print('开始保存')
        for img,title in zip(img_list,title_list):
            try:
                self.id += 1
                title = title.string
                img = img['xsrc']
                self.row += 1
                # 保存文字
                self.wooksheet.write(self.row, self.col, title)
                # 下载图片并保存
                imgContent = requests.get(img)
                with open('/var/www/html/python/img/'+str(self.id)+'.jpg', 'wb') as f:
                    print('写入成功第'+str(self.id)+"个")
                    # 保存图片到文件夹
                    f.write(imgContent.content)
                    # 保存图片信息到excel中
                    self.wooksheet.write(self.row, self.col+2, str(self.id)+'.jpg')
            except:
                print('出错了')

    # 主调度函数
    def main(self):
        self.wookbook = xlsxwriter.Workbook('/var/www/html/python/cy.xlsx')
        self.wooksheet = self.wookbook.add_worksheet()
        self.wooksheet.write(self.row, self.col, '标题')
        self.wooksheet.write(self.row, self.col+1, '解释')
        self.wooksheet.write(self.row, self.col+2, '图片名称')
        for url in self.urlList:
            self.downLoad(url)
        self.wookbook.close()


# 入口函数
if __name__ == "__main__":
    urlList = ["http://ccy.72g.com"]
    craw = Spider(urlList)
    craw.main()