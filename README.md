# My_Portfolio Project

## 本專案使用 mac os

## before start: init empty repository in project

```bash
$ mkdir flask_project # 建立專案資料夾
$ cd flask_project # 進入該專案資料夾
$ git init # 在本地數據庫-建立空儲存庫

$ mkdir web_server
$ cd web_server
$ touch index.html style.css script.js;code .
```

## Setting Up Flask

### 1. Create an virtural environment:

#### 常見做法：

```bash
$ python3 -m venv .venv # =>通常作法
# `-m` 參數告訴 Python 執行一個模組module
# `venv` 用於創建虛擬環境的內置模組
# 指定虛擬環境的目錄名稱`.venv`
```

#### 我這次做法是：

```bash
$ cd .. # 從web_server去到上ㄧ層 #Flask_project
$ python3 -m venv web\_server/ # 在#Flask_project這裡指定虛擬環境的目錄名稱是 web_server => 要記得寫 web\_server/ ,"\_"代表後面這個下劃線的字元不能忽略 才能指定`web_server`資料夾為虛擬環境的目錄名稱
```

### 2. Activate the virtural environment

```bash
# 以下指令適用於mac os / linux
$ source web\_server/bin/activate # 在bin資料夾下有一個activate可執行檔
```

```bash
#Done activated(below)
(web_server) [~/flask_project]
```

### 3.Install Flask

```bash
$ pip --version
# make sure sure the version of the pip3
```

```bash
$ pip install Flask # installing Flask
```

### 4.Building A Flask Server

## A Minimal Application

### create a new python file in web_server directory

```bash
$ cd web_server
$ touch server.py
```

- 在 server.py 檔案中寫以下程式碼：

```python
from flask import Flask # 導入Flask類(說明書) -> WSGI 應用程式

app = Flask(__name__) # 透過Flask類說明書 -> 創建app物件

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

## reference

- 詳請可見[Flask](https://flask.palletsprojects.com/en/3.0.x/installation/)
- 詳請可見[venv Documentation](https://docs.python.org/3/library/venv.html)
