import logging
import time
import tkinter as tk
from tkinter import messagebox, ttk

from concurrent.futures import ThreadPoolExecutor

from spider import Spider


# User interface class
class GUI:
    def __init__(self):
        self.spider = Spider([], [])

        self.window = tk.Tk()
        self.window.title('Spider')
        self.window.geometry('1800x600')

        # Top area frame
        top_area_frame = tk.Frame(self.window)
        top_area_frame.pack(side='top', padx=10, pady=10)

        # System time label
        self.system_time_label = tk.Label(top_area_frame, text='')
        self.system_time_label.pack(side='left')

        # Run button
        run_button = tk.Button(top_area_frame, text='Run', command=self.on_start, bg="white", fg="black", width=10,
                               height=2)
        run_button.pack(side='left', padx=10)

        # A Part: Keyword frame
        keyword_frame = tk.Frame(self.window)
        keyword_frame.pack(side='left', padx=10, pady=10)

        keyword_label = tk.Label(keyword_frame, text='Keywords:')
        keyword_label.pack(side='top', padx=10, pady=10)

        self.keyword_listbox = tk.Listbox(keyword_frame, width=30)
        self.keyword_listbox.pack(side='top', padx=10)

        # New frame for keyword entry and buttons
        keyword_entry_frame = tk.Frame(keyword_frame)
        keyword_entry_frame.pack(side='top', padx=10, pady=10)

        keyword_entry = ttk.Entry(keyword_entry_frame, width=30)
        keyword_entry.pack(side='left', padx=10, pady=10)
        self.keyword_entry = keyword_entry

        add_keyword_button = tk.Button(keyword_entry_frame, text='Add', command=self.on_add_keyword, width=10)
        add_keyword_button.pack(side='left', padx=5)

        remove_keyword_button = tk.Button(keyword_entry_frame, text='Remove', command=self.on_remove_keyword, width=10)
        remove_keyword_button.pack(side='left', padx=5)

        # B Part: URL frame
        url_frame = tk.Frame(self.window)
        url_frame.pack(side='left', padx=10, pady=10)

        url_label = tk.Label(url_frame, text='URLs:')
        url_label.pack(side='top', padx=10, pady=10)

        self.url_listbox = tk.Listbox(url_frame, width=30)
        self.url_listbox.pack(side='top', padx=10)

        # New frame for URL entry and buttons
        url_entry_frame = tk.Frame(url_frame)
        url_entry_frame.pack(side='top', padx=10, pady=10)

        url_entry = ttk.Entry(url_entry_frame, width=30)
        url_entry.pack(side='left', padx=10, pady=10)
        self.url_entry = url_entry

        add_url_button = tk.Button(url_entry_frame, text='Add', command=self.on_add_url, width=10)
        add_url_button.pack(side='left', padx=5)

        remove_url_button = tk.Button(url_entry_frame, text='Remove', command=self.on_remove_url, width=10)
        remove_url_button.pack(side='left', padx=5)

        # C Part: Log display box
        log_frame = tk.Frame(self.window)
        log_frame.pack(side='top', padx=10, pady=10, fill='both', expand=True)

        log_label = tk.Label(log_frame, text='Log:')
        log_label.pack(side='top', padx=10, pady=10)

        self.log_text = tk.Text(log_frame, wrap='word', width=30, height=10, state='disabled')
        self.log_text.pack(side='top', padx=10, pady=10, fill='both', expand=True)

        # Set default URL and keyword
        url_entry.insert(0, 'https://www.example.com')
        keyword_entry.insert(0, 'example')

    def run(self):
        self.update_system_time()
        self.window.mainloop()

    def update_system_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.system_time_label.config(text=f'System Time: {current_time}')
        self.window.after(1000, self.update_system_time)

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

    def on_start(self):
        if not self.spider.urls:
            messagebox.showerror('Error', 'Please add at least one URL')
            return
        if not self.spider.keywords:
            messagebox.showerror('Error', 'Please add at least one keyword')
            return

        # Clear results and logs
        self.spider.results = {}
        self.log_text.delete('1.0', 'end')

        # Start spider
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.spider.start)

        # Update log display
        logging.basicConfig(level=logging.INFO, stream=self.log_text)

    def on_stop(self):
        self.spider.stop_event.set()
        logging.info('Spider stopped')


if __name__ == '__main__':
    gui = GUI()
    gui.run()
 
