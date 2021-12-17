from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree
import csv




def get_onePage_info(web):
    web.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    page_text = web.page_source

    # 进行解析
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//li[contains(@class,"gl-item")]')
    book_infos = []
    for li in li_list:
        book_name = ''.join(
            li.xpath('.//div[@class="p-name"]/a/em/text()'))     # 书名
        price = '￥' + \
            li.xpath('.//div[@class="p-price"]/strong/i/text()')[0]   # 价格
        author_span = li.xpath('.//span[@class="p-bi-name"]/a/text()')
        if len(author_span) > 0:  # 作者
            author = author_span[0]
        else:
            author = '无'
        store_span = li.xpath(
            './/span[@class="p-bi-store"]/a[1]/text()')  # 出版社
        if len(store_span) > 0:
            store = store_span[0]
        else:
            store = '无'
        img_url_a = li.xpath('.//div[@class="p-img"]/a/img')[0]
        if len(img_url_a.xpath('./@src')) > 0:
            img_url = 'https' + img_url_a.xpath('./@src')[0]  # 书本图片地址
        else:
            img_url = 'https' + img_url_a.xpath('./@data-lazy-img')[0]
        one_book_info = [book_name, price, author, store, img_url]
        book_infos.append(one_book_info)
    return book_infos


def main():
    web = webdriver.Edge("msedgedriver.exe")
    web.get('https://www.jd.com/')
    web.maximize_window()
    web.find_element_by_id('key').send_keys('计算机图形学', Keys.ENTER)  
    time.sleep(2)
    all_book_info = []
    for i in range(0, 3):
        all_book_info += get_onePage_info(web)
        print('爬取第' + str(i+1) + '页成功')
        web.find_element_by_class_name('pn-next').click()  # 点击下一页
        time.sleep(2)
    with open('计算机图形学.csv', 'w', encoding='utf-8')as fp:
        writer = csv.writer(fp)
        writer.writerow(['书名', '价格', '作者', '出版社', '预览图片地址'])
        writer.writerows(all_book_info)

if __name__ == '__main__':
    main()
