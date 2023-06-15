# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import http.cookiejar, urllib.request
from urllib.request import urlretrieve
from time import sleep
import asyncio, pickle, os, re, json
from pyppeteer import launch
from urllib.parse import urlparse


class Xfuedu:

    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        self.site = "http://www.target_site_url.com:8070"
        self.home_url = "http://www.target_site_url.com:8070/index.php"
        self.login_url = "http://www.target_site_url.com:8070/logging.php?action=login"
        self.chapter_url = "http://www.target_site_url.com:8070/forumdisplay.php?fid=84&page=2"
        self.download_url = "http://www.target_site_url.com:8070/attachment.php?aid=11115"
        self.browser = False
        self.feeds = []
        self.tabs = []

    def save_cookies(self, cookies, site):
        cookies_path = os.path.join(self.script_dir, "cookies")
        os.makedirs(cookies_path, exist_ok=True)
        saved_cookies_path = os.path.join(cookies_path,
                                          re.sub(r"[^\w\.-]", "_", site) + ".pkl")
        
        with open(saved_cookies_path, 'wb') as file:
            pickle.dump(cookies, file)

    def load_cookies(self, site):
        try:
            cookies_path = os.path.join(self.script_dir, "cookies")
            saved_cookies_path = os.path.join(cookies_path,
                                              re.sub(r"[^\w\.-]", "_", site) + ".pkl")
            with open(saved_cookies_path, 'rb') as file:
                cookies = pickle.load(file)
                if isinstance(cookies, list):
                    return cookies
                else:
                    raise Exception("Cookies 格式不正确")
        except:
            return []

    async def close(self):
        await self.browser.close()
        self.browser = False
        await asyncio.sleep(3)

    async def new_tab(self, url):
        if (self.browser == False):
            self.browser = await launch(headless=True,
                                        devtools=False,
                                        defaultViewport={
                                            'width': 1920,
                                            'height': 1080
                                        })

        page = await self.browser.newPage()
        await page.setUserAgent(self.user_agent)

        parsed_url = urlparse(url)
        host = parsed_url.netloc

        cookies = self.load_cookies(host)
        for cookie in cookies:
            await page.setCookie(cookie)

        await page.goto(url)
        await asyncio.sleep(5)
        cookies = await page.cookies()
        self.save_cookies(cookies, host)
        self.tabs.append(page)
        if(len(self.tabs) > 4):
            await self.tabs[0].close()
            del(self.tabs[0])
        return page

    async def get_html_raw(self, url, auto_close=False):
        page = await self.new_tab(url)
        html_content = await page.content()
        if(auto_close == True):
            await page.close()
        await asyncio.sleep(1)
        return html_content

    async def login(self):
        page = await self.new_tab(self.login_url)
        username_input = 'body > center > div.maintable > form > div.spaceborder > table > tbody > tr:nth-child(2) > td.altbg2 > span > input[type="text"]'
        password_input = 'body > center > div.maintable > form > div.spaceborder > table > tbody > tr:nth-child(3) > td.altbg2 > span > input[type="password"]'
        submit_btn = 'body > center > div.maintable > form > div.option > div > input'
        await page.type(username_input, "", { "delay": 10 })
        await page.type(password_input, "", { "delay": 10 })
        await page.click(submit_btn)
        await asyncio.sleep(5)

    async def get_list(self):
        raw_html = await self.get_html_raw(self.chapter_url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        chapter_list = soup.find_all("td", class_="f_title")
        
        feeds = []

        for link_arr in chapter_list:
            links = link_arr.find_all("a")
            if(len(links) >= 1):
                title = links[0].get_text()
                href = links[0].get("href").replace("&extra=page%3D2","")
                url = f"{self.site}/{href}"
                feeds.append({
                    "title": title,
                    "url": url,
                })
                print(f"{title}{url}")
        self.feeds = feeds

    def get_next_page(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

        next_page = soup.find(class_="section-opt m-bottom-opt").find(
            "a", string="下一页")
        if (next_page is not None):
            url = self.site + next_page.get("href")
            return url
        else:
            return None

    def collect_text(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        content = soup.find_all(class_="t_msgfont")
        if(len(content) >= 1):
            return content[0].get_text()
        else:
            return ""

    async def get_content(self, article_url):
        content = ""
        raw_html = await self.get_html_raw(article_url)
        content = self.collect_text(raw_html)
        return re.sub(r'\n+', '\n', content)

    async def save_book(self, book_name, content):
        book_path = os.path.join(self.script_dir, "book")
        os.makedirs(book_path, exist_ok=True)
        modified_book_name = re.sub(r"[^\w\.-]", "_", book_name)
        file_path = os.path.join(book_path, modified_book_name + ".txt")
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)

    async def save_all(self, book_name):
        max_len = len(self.feeds)
        for index, feed in enumerate(self.feeds):
            content = await self.get_content(feed["url"])
            content = feed["title"] + "\n" + content
            await self.save_book(book_name, content)
            print(f"[{index}/{max_len}] " + feed["url"])
            await asyncio.sleep(10)
        return

    async def download(self, url, filename):
        # filepath
        file_path = os.path.join(self.script_dir, "download")
        os.makedirs(file_path, exist_ok=True)
        file_name = re.sub(r"[^\w\.-]", "_", filename)
        file_path = os.path.join(file_path, file_name + ".rar")

        # cookies
        parsed_url = urlparse(url)
        host = parsed_url.netloc

        def cookie_from_dict(d):
            return http.cookiejar.Cookie(**d)
        
        cookies = self.load_cookies(host)

        # 调用http方法中的cookieJar方法来自动存储cookie
        cookie_jar = http.cookiejar.CookieJar()

        for cookie in cookies:
            list = [] # tuple
            for key in cookie:
                list.append(cookie[key])
            ck = http.cookiejar.Cookie(
                0,
                cookie["name"],
                cookie["value"],
                None,
                False,
                cookie["domain"],
                False,
                False,
                cookie["path"],
                False,
                False,
                cookie["expires"],
                False,
                None,
                None,
                cookie,
                False,
            )
            print(cookie)
            # print(http.cookiejar.Cookie((cookie)))
            cookie_jar.set_cookie(ck)
        # 创建可以调用cookieJar 的处理器, 传递cookie_jar
        cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)

        # 根据处理器生成相应的opener
        opener = urllib.request.build_opener(cookie_handler)
        opener.addheaders = [
            ('User-agent', self.user_agent),
            ('Cookies', "cdb_visitedfid=84D82; is_use_cookied=yes; is_use_cookiex=yes; cdb_sid=8DpX3P; cdb_oldtopics=D2302881D"),
        ]
        urllib.request.install_opener(opener)
        
        def progress(a,b,c):  
            per = 100.0 * a * b / c  
            if per > 100:  
                per = 100  
            print('%.2f%%' % per)
        
        print(url)
        urlretrieve(url, file_path, progress)

    async def get_download_url(self, url):
        raw_html = await self.get_html_raw(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        link = soup.find("div", class_="t_attachlist").find("a")
        return self.site + "/" + link.get("href")
        
    async def download_all(self):
        max_len = len(self.feeds)
        for index, feed in enumerate(self.feeds):
            download_link = await self.get_download_url(feed["url"])
            await self.download(download_link, feed["title"])
            print(f"[{index}/{max_len}] " + feed["url"])
            await asyncio.sleep(10)
        return
async def main():
    br = Xfuedu()
    # await br.login()
    await br.get_list()
    await br.download_all()
    # await br.save_all("maya")
    # await br.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已终止")
