import requests
import tkinter as tk
from tkinter import messagebox
import time
from urllib.parse import quote

counter = int(time.time() * 1000)
data = {
    'callback': 'dr' + str(counter),
    '_': str(counter)
}

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': '192.168.8.123',
    'Referer': 'http://192.168.8.123/',
    'User-Agent': 'Mozilla/5.0'
}

url = (
    'http://192.168.8.123/drcom/logout?callback=' +
    quote(data['callback']) + '&_=' + quote(data['_'])
)

try:
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        messagebox.showinfo('提示', '已下线（Code:200）')
    else:
        messagebox.showerror('失败', f'下线失败（Code:{response.status_code}）')
except Exception as e:
    messagebox.showerror('异常', str(e))
