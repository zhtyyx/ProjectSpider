import sys
import tkinter as tk
from tkinter import ttk, font

from spider import Spider, search_google
from utils import get_html, save_to_file, sanitize_filename


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.configure(state='normal')
        self.widget.insert('end', text)
        self.widget.see('end')
        self.widget.configure(state='disabled')

    def flush(self):
        pass


# User interface class
class GUI:
    def __init__(self):
        self.spider = Spider([], [])

        self.window = tk.Tk()
        self.window.title('Spider')
        self.window.geometry('1500x800')
        # 设置默认字体大小
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=int(default_font.cget("size") * 1.2))

        # PanedWindow for three modules
        paned_window = ttk.PanedWindow(self.window, orient='horizontal')
        paned_window.pack(side='top', fill='both', expand=True)

        # A Part: Google Spider frame
        google_spider_frame = tk.Frame(paned_window)
        paned_window.add(google_spider_frame, weight=1)
        google_spider_label = tk.Label(google_spider_frame, text='Google Spider', font=('TkDefaultFont', 14, 'bold'))
        google_spider_label.pack(side='top', padx=10, pady=10)
        # Search Word label and entry
        search_word_label = tk.Label(google_spider_frame, text='Search Word:')
        search_word_label.pack(side='top', padx=10, pady=10, anchor='w')

        search_word_entry = ttk.Entry(google_spider_frame, width=30)
        search_word_entry.pack(side='top', padx=10, pady=10, anchor='w')
        self.search_word_entry = search_word_entry

        keyword_label = tk.Label(google_spider_frame, text='Keywords:', anchor='w')
        keyword_label.pack(side='top', padx=10, pady=10, fill='x')

        # New frame for keyword entry and buttons
        keyword_entry_frame = tk.Frame(google_spider_frame)
        keyword_entry_frame.pack(side='top', padx=10, pady=10, anchor='w')

        keyword_entry = ttk.Entry(keyword_entry_frame, width=30)
        keyword_entry.pack(side='left', padx=10, pady=10, anchor='w')
        self.keyword_entry = keyword_entry

        add_keyword_button = tk.Button(keyword_entry_frame, text='Add', command=self.on_add_keyword, width=10)
        add_keyword_button.pack(side='left', padx=5)

        remove_keyword_button = tk.Button(keyword_entry_frame, text='Remove', command=self.on_remove_keyword, width=10)
        remove_keyword_button.pack(side='left', padx=5)

        self.keyword_listbox = tk.Listbox(google_spider_frame, width=30)
        self.keyword_listbox.pack(side='top', padx=10, anchor='w')

        page_label = tk.Label(google_spider_frame, text='Pages:', anchor='w')
        page_label.pack(side='top', padx=10, pady=10, fill='x')

        page_entry = ttk.Entry(google_spider_frame, width=30)
        page_entry.pack(side='top', padx=10, pady=10, anchor='w')
        self.page_entry = page_entry

        run_google_button = tk.Button(google_spider_frame, text='Run Google Spider', command=self.on_start_google,
                                      bg="white", fg="black", width=20,
                                      height=2)
        run_google_button.pack(side='bottom', padx=10)

        # 分割线
        separator = ttk.Separator(paned_window, orient='vertical')
        paned_window.add(separator)

        # B Part: Site Spider frame
        site_spider_frame = tk.Frame(paned_window)
        paned_window.add(site_spider_frame, weight=1)

        site_spider_label = tk.Label(site_spider_frame, text='Site Spider', font=('TkDefaultFont', 14, 'bold'))
        site_spider_label.pack(side='top', padx=10, pady=10)

        site_keyword_label = tk.Label(site_spider_frame, text='Keywords:', anchor='w')
        site_keyword_label.pack(side='top', padx=10, pady=10, anchor='w')

        # New frame for keyword entry and buttons
        site_keyword_entry_frame = tk.Frame(site_spider_frame)
        site_keyword_entry_frame.pack(side='top', padx=10, pady=10)

        site_keyword_entry = ttk.Entry(site_keyword_entry_frame, width=30)
        site_keyword_entry.pack(side='left', padx=10, pady=10, anchor='w')
        self.site_keyword_entry = site_keyword_entry

        add_site_keyword_button = tk.Button(site_keyword_entry_frame, text='Add', command=self.on_add_site_keyword,
                                            width=10)
        add_site_keyword_button.pack(side='left', padx=5)

        remove_site_keyword_button = tk.Button(site_keyword_entry_frame, text='Remove',
                                               command=self.on_remove_site_keyword, width=10)
        remove_site_keyword_button.pack(side='left', padx=5)

        self.site_keyword_listbox = tk.Listbox(site_spider_frame, width=30)
        self.site_keyword_listbox.pack(side='top', padx=10, anchor='w')

        url_label = tk.Label(site_spider_frame, text='URLs:')
        url_label.pack(side='top', padx=10, pady=10, anchor='w')

        # New frame for URL entry and buttons
        url_entry_frame = tk.Frame(site_spider_frame)
        url_entry_frame.pack(side='top', padx=10, pady=10)

        url_entry = ttk.Entry(url_entry_frame, width=30)
        url_entry.pack(side='left', padx=10, pady=10)
        self.url_entry = url_entry

        add_url_button = tk.Button(url_entry_frame, text='Add', command=self.on_add_url, width=10)
        add_url_button.pack(side='left', padx=5)

        remove_url_button = tk.Button(url_entry_frame, text='Remove', command=self.on_remove_url, width=10)
        remove_url_button.pack(side='left', padx=5)

        self.url_listbox = tk.Listbox(site_spider_frame, width=30)
        self.url_listbox.pack(side='top', padx=10, anchor='w')

        run_site_button = tk.Button(site_spider_frame, text='Run Site Spider', command=self.on_start_site, bg="white",
                                    fg="black", width=20,
                                    height=2)
        run_site_button.pack(side='bottom', padx=10)

        # C Part: Log display box
        log_frame = tk.Frame(paned_window)
        paned_window.add(log_frame, weight=1)

        log_label = tk.Label(log_frame, text='Log:')
        log_label.pack(side='top', padx=10, pady=10, anchor='w')

        self.log_text = tk.Text(log_frame, wrap='word', state='disabled')
        self.log_text.pack(side='top', padx=10, pady=10, fill='both', expand=True)

        sys.stdout = TextRedirector(self.log_text)

    def run(self):
        self.window.mainloop()

    def on_add_url(self):
        url = self.url_entry.get()
        if url not in self.spider.urls:
            self.spider.add_url(url)
            self.url_listbox.insert('end', url)

    def on_remove_url(self):
        selected = self.url_listbox.curselection()
        if selected:
            index = selected[0]
            url = self.url_listbox.get(index)
            self.spider.remove_url(url)
            self.url_listbox.delete(index)

    def on_add_keyword(self):
        keyword = self.keyword_entry.get()
        if keyword not in self.spider.keywords:
            self.spider.keywords.append(keyword)
            self.keyword_listbox.insert('end', keyword)

    def on_remove_keyword(self):
        selected = self.keyword_listbox.curselection()
        if selected:
            index = selected[0]
            keyword = self.keyword_listbox.get(index)
            self.spider.keywords.remove(keyword)
            self.keyword_listbox.delete(index)

    def on_add_site_keyword(self):
        keyword = self.site_keyword_entry.get()
        if keyword not in self.spider.keywords:
            self.spider.keywords.append(keyword)
            self.site_keyword_listbox.insert('end', keyword)

    def on_remove_site_keyword(self):
        selected = self.site_keyword_listbox.curselection()
        if selected:
            index = selected[0]
            keyword = self.site_keyword_listbox.get(index)
            self.spider.keywords.remove(keyword)
            self.site_keyword_listbox.delete(index)

    def on_start_google(self):
        # 示例
        api_key = 'AIzaSyAp_sCxfWFQDaPePlXynuwWZ6B6O-po5xg'
        cse_id = 'a55272e9ae1ae4076'
        # 获取 Search Word 的值
        search_word = self.search_word_entry.get()

        # 获取 Keywords 的值
        keywords = [self.keyword_listbox.get(i) for i in self.keyword_listbox.curselection()]

        # 获取 Pages 的值
        pages = self.page_entry.get()

        urls = search_google(api_key, cse_id, search_word, pages)
        for i, url in enumerate(urls):
            html = get_html(url)
            for keyword in keywords:
                if keyword in html:
                    print("{} found in link: {}".format(keyword, url))
            filename = f'{url}.html'
            filename = sanitize_filename(filename)
            save_to_file(filename, html)

    def on_start_site(self):
        # 获取 Keywords 的值
        keywords = [self.keyword_listbox.get(i) for i in self.keyword_listbox.curselection()]
        urls = [self.url_listbox.get(i) for i in self.url_listbox.curselection()]

        for i, url in enumerate(urls):
            html = get_html(url)
            for keyword in keywords:
                if keyword in html:
                    print("{} found in link: {}".format(keyword, url))
            filename = f'{url}.html'
            filename = sanitize_filename(filename)
            save_to_file(filename, html)


if __name__ == '__main__':
    gui = GUI()
    gui.run()
