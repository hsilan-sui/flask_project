# 使用官方的 Python 基礎映像
FROM python:3.12-slim

# 設置工作目錄
WORKDIR /app

# 複製需求文件
COPY requirements.txt requirements.txt

# 安裝需求
RUN pip install --no-cache-dir -r requirements.txt


# 複製 Flask 專案到容器中
COPY . .

# 設置環境變數以告知 Flask 應用運行在 Docker 容器內
ENV FLASK_APP=web_server/server.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露 Flask 使用的端口
EXPOSE 5000

# 運行 Flask 應用
CMD ["flask", "run"]
