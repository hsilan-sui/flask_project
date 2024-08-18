# 使用官方的 Python 基础映像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制需求文件
COPY requirements.txt requirements.txt

# 安装需求
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 复制 Flask 项目到容器中
COPY . .

# 设置时区
ENV TZ=Asia/Taipei

# 暴露端口
EXPOSE 5001

# 使用 gunicorn 启动 Flask 应用
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "web_server.server:app"]
