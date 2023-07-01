import json
from concurrent.futures import ThreadPoolExecutor

import requests
import re
import threading
import queue
import logging


# 爬虫类
class Spider:
    def __init__(self, urls, keywords):
        self.urls = urls
        self.keywords = keywords
        self.results = {}
        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

    # 添加URL
    def add_url(self, url):
        self.urls.append(url)

    # 删除URL
    def remove_url(self, url):
        self.urls.remove(url)

    # 配置关键词
    def set_keywords(self, keywords):
        self.keywords = keywords

    # 获取所有结果
    def get_results(self):
        return self.results

    # 开始爬取
    def start(self):
        # 初始化队列
        for url in self.urls:
            self.queue.put(url)
        # 创建线程池进行爬取
        with ThreadPoolExecutor(max_workers=10) as executor:
            while not self.queue.empty():
                url = self.queue.get()
                executor.submit(self.crawl, url)

    # 爬取网页
    def crawl(self, url):
        try:
            logging.info('Crawling %s', url)
            response = requests.get(url)
            if response.status_code == 200:
                print(response.text)
                self.extract_results(response.text, url)
        except Exception as e:
            logging.error('Error: %s', e)

    # 提取结果
    def extract_results(self, text, url):
        # 匹配关键词
        for keyword in self.keywords:
            if re.search(keyword, text, re.IGNORECASE):
                with self.lock:
                    self.results.setdefault(url, []).append(keyword)


def search_google(api_key, cse_id, query, page=1):
    if not page:
        page = 1
    for i in range(int(page)):
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&start={i}"
        print(url)
        response = requests.get(url)
        results = json.loads(response.text)
        urls = [item['link'] for item in results['items']]
        return urls
