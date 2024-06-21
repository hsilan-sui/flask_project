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

![虛擬環境的目錄建置](./images/venv.png)

### 2. Activate the virtural environment

```bash
# 以下指令適用於mac os / linux
$ source web\_server/bin/activate # 在bin資料夾下有一個activate可執行檔
```

```bash
#Done activated(below)
(web_server) [~/flask_project]
```

![執行虛擬環境](./images/activate-venv.png)

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

### create a new python file(server.py) in web_server directory

```bash
$ cd web_server
$ touch server.py
```

- 在 server.py 檔案中寫以下程式碼：

```python
from flask import Flask # 導入Flask類(說明書) -> WSGI 應用程式

app = Flask(__name__) # 透過Flask類說明書 -> 創建app物件

@app.route("/") # route() is a decorator to tell Flask what URL should trigger my function(request this route -> to run below the function -> return something)
def hello_user(): #The function returns the message I want to display in the user’s browser
    return "<p>妳好 sui/p>"
    #The default content type is HTML
```

### To run this application

```bash
$ flask --app server run # 是告訴flask 運行server.py這個應用程式

#舊版
$ export FLASK_APP=server
$ flask run
```

![啟動伺服器](./images/server.png)

#### Debug Mode

- 在本地端運行伺服器時，可以看到訊息寫：
  - Debug mode: off
- 可以這樣將調試器打開(加入副指令 --debug):

```bash
$ flask --app server run --debug
#舊版 除錯模式
$ export FLASK_APP=development
$ flask run

```

> [!WARNING]
> The debugger allows executing arbitrary Python code from the browser. It is protected by a pin, but still represents a major security risk. Do not run the development server or debugger in a production environment.

## Try to visit some routes

### route() decorator will bind the function to return some specific vale

```python
@app.route('/blog')
def blog():
    return 'This is my first blog'

@app.route('/blog/ca2020/job')
def blog2():
    return 'This is my first job!!!'
```

## Rendering Templates

![render-template](./images/render-template.png)

- To render a template,use the render_template() method

  - this render_template() allow me to send the HTML file
  - how it works?

    - Flask will look for templates file in the "templates" folder
    - if u application is a module, this folder is next to that module (my server.py is a module)=> this way
    - if it’s a package it’s actually inside your package

```
/web_server (創建的虛擬環境)
  /server.py  (模組)
  /templates (templates資料夾＝>一定要創建)
    /index.html (想要渲染在瀏覽器的html內容)
```

![建立templates檔案夾](./images/templates-dir.png)

```python
@app.route("/aboutMe.html")
def aboutMe():
    return render_template('aboutMe.html')
```

## Static Files

- Dynamic web applications also need "Static Files" it's where the CSS and JavaScript files are coming from.
- my flask web server is configured to serve them
- but during development, Flask can do that as well.
- Just create a folder called "static" in your package or next to your module and it will be available at /static on the application

### what to do ?

- at first, create directory named "static" just below the web_server/ also besides my server.py module
- second, I move the "web_server/script.js" and "web_server/style.css" to :

  - web_server/static/script.js
  - web_server/static/style.css

- Don't forget to fix the link about CSS and JS in index.html file

## Adding a favicon

- favicon is an icon used by browsers for tabs and bookmarks

### how to add a favicon to a Flask application

- prepare icon:

  - icon size: 16 × 16 pixels
  - in the ICO file format
  - Put the icon in static directory as favicon.ico

- get browsers to find your icon:
  - to generate URLs for static files, use the special 'static' endpoint name
  ```html
  url_for('static', filename='style.css')
  ```
  - add a link tag in HTML file
  ```html
  <link
    rel="shortcut icon"
    href="{{ url_for('static', filename='favicon.ico') }}"
  />
  ```

## Templating Engine & Variable Rules

### Templating Engine

- we can use flask to build things dynamiclly.
- if I do in index.html like this:

```html
<body>
  {{4 + 5}}
</body>
```

- flask 會當作是表達式(python code) =>運算結果
- jinja 是 flask 預設的 Template Engine

### Variable Rules

- 如何動態的新增名字在 url 中並且能夠動態的連動改變在 html 顯示的變數內容：

```python
@app.route('/<myname>')
def hello(myname=None):
  return render_template('index.html', name=myname)
```

- html 檔案要這樣設定：

```html
<body>
  <h1>hello {{name}}</h1>
</body>
```

- 還可以指定變數參數的類型：

```python
@app.route('/<myname>/<int:post_id>')
def hello(myname=None, post_id=None):
  return render_template('index.html', name=myname, post_id=post_id)
```

- html 加入變數:

```html
<body>
  <h1>hello hahaha 終於成功！ {{5 + 5}} {{name}} {{post_id}}</h1>
  <script src="static/script.js"></script>
</body>
```

![動態顯示](./images/dynmic.png)

## reference

- 詳請可見[Flask](https://flask.palletsprojects.com/en/3.0.x/installation/)
- 詳請可見[venv Documentation](https://docs.python.org/3/library/venv.html)
