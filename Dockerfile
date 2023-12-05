# 使用 Python 的官方基础镜像
FROM python:slim

# 设置工作目录
WORKDIR /usr/src/app

# 复制项目文件和文件夹到工作目录
COPY . .

# 安装依赖
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install --no-cache-dir -r requirements.txt

# 应用运行在哪个端口
EXPOSE 60000

# 运行应用
CMD ["python3", "./server.py"]
