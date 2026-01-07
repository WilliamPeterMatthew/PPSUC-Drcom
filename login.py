import os
import sys
import requests
import tkinter as tk
from tkinter import messagebox
import time
from urllib.parse import quote
from bs4 import BeautifulSoup

base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
account_file = os.path.join(base_dir, '账号密码.txt')

def load_account():
    if os.path.exists(account_file):
        try:
            with open(account_file, 'r', encoding='utf-8') as f:
                lines = [i.strip() for i in f.readlines() if i.strip()]
            if len(lines) >= 2:
                return lines[0], lines[1]
        except:
            pass
    return None, None

def input_ui():
    result = {}

    def submit():
        result['user'] = entry_user.get().strip()
        result['pwd'] = entry_pwd.get().strip()
        win.destroy()

    win = tk.Tk()
    win.title('网络登录')
    win.geometry('300x160')
    win.resizable(False, False)

    tk.Label(win, text='账号').pack(pady=5)
    entry_user = tk.Entry(win)
    entry_user.pack()

    tk.Label(win, text='密码').pack(pady=5)
    entry_pwd = tk.Entry(win, show='*')
    entry_pwd.pack()

    tk.Button(win, text='登录', command=submit).pack(pady=15)

    win.mainloop()
    return result.get('user'), result.get('pwd')

username, password = load_account()
if not username or not password:
    username, password = input_ui()

if not username or not password:
    messagebox.showerror('错误', '账号或密码不能为空')
    sys.exit(0)

counter = int(time.time() * 1000)
data = {
    'callback': 'dr' + str(counter),
    'DDDDD': username,
    'upass': password,
    '0MKKey': '12346',
    'R1': '0',
    'R3': '0',
    'R6': '0',
    'para': '00',
    'v6ip': '',
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
    'http://192.168.8.123/drcom/login?callback=' + quote(data['callback']) +
    '&DDDDD=' + quote(data['DDDDD']) +
    '&upass=' + quote(data['upass']) +
    '&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip=&_=' + quote(data['_'])
)

try:
    response = requests.post(url, data=data, headers=headers, timeout=5)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ''
        if title == '认证成功页':
            messagebox.showinfo('成功', '已连接（Code:200）')
        else:
            messagebox.showerror('失败', '账号或密码不正确')
    else:
        messagebox.showerror('失败', f'连接失败（Code:{response.status_code}）')
except Exception as e:
    messagebox.showerror('异常', str(e))
