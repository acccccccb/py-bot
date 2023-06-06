# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


def get_content(url):
    response = urllib.request.Request(url, headers=headers)
    response.add_header('Referer', 'http://www.xfuedu.org/bxwx/28342/')
    response = urllib.request.urlopen(url)
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.find(id="content").get_text("<br/>", strip=True).replace(
        '<br/>', "\n").replace("章节错误,点此举报(免注册)",
                               "").replace(",举报后维护人员会在两分钟内校正章节内容,请耐心等待,并刷新页面。",
                                           "")
    print(f"{content}")


def get_chapter_list():
    url = "http://www.xfuedu.org/bxwx/28342/"
    response = urllib.request.Request(url)
    response.add_header('Referer', 'http://www.xfuedu.org/')
    response = urllib.request.urlopen(url)
    print(f"{response.getcode()}")
    html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    chapter_list = soup.find_all("ul",
                                 class_="section-list fix")[1].find_all("a")
    # chapter_list.reverse()

    options = []

    for index, link in enumerate(chapter_list):
        # chapter_url = "[" + str(
        #     index) + "] - " + link.get_text() + " - " + url + link.get("href")
        options.append({
            "title": link.get_text(),
            "url": url + link.get("href")
        })
        # print(f"{chapter_url}")
    current_option = 0
    # 打印选项列表
    for i, option in enumerate(options):
        if i == current_option:
            print(f'> {i}-{option["title"]}')
        else:
            print(f'  {i}-{option["title"]}')

    # 获取用户输入
    key = input('input and enter: ')
    get_content(options[int(key)]["url"])
    # 处理回车键
    # if key == 'enter':
    # selected_option = options[current_option]
    # get_content(selected_option["url"])
    # break


get_chapter_list()