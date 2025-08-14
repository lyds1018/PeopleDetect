# 1) 基础镜像
FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
        python3 python3-pip \
        libgl1 \
        libglib2.0-0 \
        libsm6 libxext6 libxrender1 libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# 4) 创建工作目录
WORKDIR /workspace

# 5) 复制代码
COPY . .

ENV PYTHONPATH=/workspace

# 6) 安装依赖
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

# 7) 声明入口：容器启动后自动执行 main_event.py
ENTRYPOINT ["python3", "/workspace/main/main_event.py"]