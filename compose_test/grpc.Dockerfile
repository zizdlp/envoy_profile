# 使用官方的 Python 镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 安装 gRPC 和 protobuf 工具
RUN pip install grpcio protobuf grpcio-reflection numpy