# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import urllib.request
from time import sleep
import asyncio, pickle, os, re
from pyppeteer import launch
from urllib.parse import urlparse


class Xfuedu:

    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        self.site = "http://www.xfuedu.org"
        self.chapter_url = "http://www.xfuedu.org/bxwx/28342/"
        self.browser = False
        self.feeds = []

    def save_cookies(self, cookies, site):
        cookies_path = os.path.join(self.script_dir, "cookies")
        os.makedirs(cookies_path, exist_ok=True)
        saved_cookies_path = os.path.join(cookies_path,
                                          site.replace(".", "_") + ".pkl")
        with open(saved_cookies_path, 'wb') as file:
            pickle.dump(cookies, file)

    def load_cookies(self, site):
        try:
            cookies_path = os.path.join(self.script_dir, "cookies")
            saved_cookies_path = os.path.join(cookies_path,
                                              site.replace(".", "_") + ".pkl")
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

    async def get_html_raw(self, url):
        if (self.browser == False):
            self.browser = await launch(headless=True,
                                        devtools=True,
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

        await asyncio.sleep(2)

        html_content = await page.content()
        cookies = await page.cookies()
        self.save_cookies(cookies, host)
        await page.close()
        await asyncio.sleep(2)
        return html_content

    async def get_list(self):
        raw_html = await self.get_html_raw(self.chapter_url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        chapter_list = soup.find_all(
            "ul", class_="section-list fix")[1].find_all("a")

        feeds = []

        for link in chapter_list:
            title = link.get_text()
            href = link.get("href")
            url = f"{self.chapter_url}{href}"
            feeds.append({
                "title": title,
                "url": url,
            })
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
        content = soup.find(id="content").get_text(
            "<br/>", strip=True).replace('<br/>', "\n").replace(
                "章节错误,点此举报(免注册)",
                "").replace(",举报后维护人员会在两分钟内校正章节内容,请耐心等待,并刷新页面。", "")
        return content

    async def get_content(self, article_url):
        content = ""
        raw_html = await self.get_html_raw(article_url)
        next_page = self.get_next_page(raw_html)
        content += self.collect_text(raw_html)

        while next_page is not None:
            raw_html = await self.get_html_raw(next_page)
            next_page = self.get_next_page(raw_html)
            content += self.collect_text(raw_html)
            await asyncio.sleep(5)

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
            await self.save_book(book_name, content)
            print(f"[{index}/{max_len}] " + feed["url"])
            await asyncio.sleep(10)


async def main():
    br = Xfuedu()
    await br.get_list()
    await br.save_all("大秦")
    await br.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已终止")
