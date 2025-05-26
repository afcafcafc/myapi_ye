FROM python:3.11-slim

# 设置工作目录
WORKDIR /root

# 安装依赖
RUN apt update && \
    apt install -y ffmpeg git python3-django python3-django-cors-headers&& \
    pip install --upgrade pip && \
    pip install django && \
    git clone https://github.com/afcafcafc/myapi_ye.git
    chmod +x /myapi_ye/N_m3u8DL-RE

# 进入项目目录
WORKDIR /root/myapi_ye

# 开放端口
EXPOSE 8000

# 启动 Django 服务
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
#python3 /root/myapi_ye/manage.py runserver 0.0.0.0:8000
