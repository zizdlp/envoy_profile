# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import time
import logging
import numpy as np 
import grpc
from concurrent.futures import ThreadPoolExecutor,as_completed
import data_pb2
import data_pb2_grpc
from multiprocessing import Process
from multiprocessing import Pool
import os
import argparse

CLIENT_ID = 1
def utf8len(s):
    return len(s.encode('utf-8'))

# 中文注释和英文翻译
# Note that this example was contributed by an external user using Chinese comments.
# In all cases, the Chinese comment text is translated to English just below it.


# # 客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
# # stream-unary (In a single call, the client can transfer data to the server several times,
# # but the server can only return a response once.)
# def bidirectional_streaming_method(stub,data):
#     # 创建一个生成器
#     # create a generator
#     def request_messages():
#         total_lens=len(data)
#         block_len=3*(1<<20) #####3MB
#         left,right=0,min(total_lens,block_len)  ###[left,right)
#         print(f"stream client send total_len:{total_lens/1024/1024}MB")
#         numBlocks=(total_lens+block_len-1)//block_len
#         for block in range(numBlocks):
#             left=block*block_len
#             right=min(left+block_len,total_lens)
#             request = data_pb2.Request(
#                             client_id=CLIENT_ID,
#                             data=data[left:right])
#             yield request

#     response_iterator = stub.BidirectionalStreamingMethod(request_messages())
#     recv_data=None
#     for response in response_iterator:
#         if recv_data:
#             recv_data+=response.data
#         else:
#             recv_data=response.data
#     print(f"stream client recv total_len:{len(recv_data)/1024/1024}MB")
#     return True
# def unary_method(stub,data):
#     print(f"unary client send total_len:{len(data)/1024/1024} MB")
#     request = data_pb2.Request(
#                             client_id=CLIENT_ID,
#                             data=data)
#     response = stub.UnaryMethod(request)
#     recv_data=response.data
#     print(f"unary client recv total_len:{len(recv_data)/1024/1024} MB")
#     return True

# 客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
# stream-unary (In a single call, the client can transfer data to the server several times,
# but the server can only return a response once.)
def bidirectional_streaming_method(stub,data,i):
    # 创建一个生成器
    # create a generator
    def request_messages():
        total_lens=len(data)
        block_len=3*(1<<20) #####3MB
        left,right=0,min(total_lens,block_len)  ###[left,right)
        # print(f"stream client {i} send total_len:{total_lens/1024/1024}MB")
        numBlocks=(total_lens+block_len-1)//block_len
        for block in range(numBlocks):
            left=block*block_len
            right=min(left+block_len,total_lens)
            request = data_pb2.Request(
                            client_id=CLIENT_ID,
                            data=data[left:right])
            yield request
    response_iterator = stub.BidirectionalStreamingMethod(request_messages())
    recv_data=None
    for response in response_iterator:
        if recv_data:
            recv_data+=response.data
        else:
            recv_data=response.data
    # print(f"stream client recv total_len:{len(recv_data)/1024/1024}MB")
    return True
def unary_method(stub,data,i):
    # print(f"unary client {i}  send total_len:{len(data)/1024/1024} MB")
    request = data_pb2.Request(
                            client_id=CLIENT_ID,
                            data=data)
    response = stub.UnaryMethod(request)
    recv_data=response.data
    # print(f"unary client recv total_len:{len(recv_data)/1024/1024} MB")
    return True
def streaming_call(SERVER_ADDRESS,times,data,options):
    with grpc.insecure_channel(SERVER_ADDRESS,options=options) as channel:
        stub = data_pb2_grpc.GRPCDemoStub(channel)
        pool=ThreadPoolExecutor(max_workers=5)
        all_task = [pool.submit(bidirectional_streaming_method, stub,data,i) for i in range(times)]
        for future in as_completed(all_task):
            data = future.result()
            # print("streaming: get page {}s success".format(data))
def unary_call(SERVER_ADDRESS,times,data,options):
    with grpc.insecure_channel(SERVER_ADDRESS,options=options) as channel:
        stub = data_pb2_grpc.GRPCDemoStub(channel)
        pool=ThreadPoolExecutor(max_workers=5)
        all_task = [pool.submit(unary_method, stub,data,i) for i in range(times)]
        for future in as_completed(all_task):
            data = future.result()
            # print("unary: get page {}s success".format(data))
def main():
    parser = argparse.ArgumentParser(description='gRPC Client Script')
    parser.add_argument('--server', type=str, default='localhost:50051', help='Server address')
    parser.add_argument('--data_size', type=int, default=1, help='package 1 is size:1MB')
    parser.add_argument('--message_length', type=int, default=1000*1024*1024, help='Max message length')
    parser.add_argument('--times', type=int, default=100, help='Number of times to call')

    args = parser.parse_args()

    logging.basicConfig()

    SERVER_ADDRESS = args.server
    MAX_MESSAGE_LENGTH = args.message_length
    options = [
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ]

    data = np.ones([1024, 1024, args.data_size], dtype="uint8")  # 100MB
    data = data.tobytes()

    s1 = time.time()
    unary_call(SERVER_ADDRESS,args.times,data, options=options)
    e1 = time.time()

    s2 = time.time()
    streaming_call(SERVER_ADDRESS,args.times,data, options=options)
    e2 = time.time()

    print(f"=====unary call {args.times} times with data_size:{args.data_size} MB: time consume:{e1-s1}")
    print(f"=====streaming call {args.times} times with data_size:{args.data_size}MB: time consume:{e2-s2}")


if __name__ == '__main__':
    main()