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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import multiprocessing
import grpc
from grpc_reflection.v1alpha import reflection
import data_pb2
import data_pb2_grpc
SERVER_ADDRESS = 'localhost:50051'
SERVER_ID = 1

class DemoServer(data_pb2_grpc.GRPCDemoServicer):
    # 客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
    # stream-unary (In a single call, the client can transfer data to the server several times,
    # but the server can only return a response once.)
    def UnaryMethod(self, request, context):
        print("=== UnaryMethod called by client:{} MB".format(len(request.data)/(1024*1024)))
        response = data_pb2.Response(
            server_id=request.client_id)
        return response

    def BidirectionalStreamingMethod(self, request_iterator, context):
        total_lens=0
        for request in request_iterator:
            total_lens+=len(request.data)
        block_len=3*(1<<20) #####3MB
        print(f"=== StreamMethod called by clinet: {total_lens/(1024*1024)} MB")
        numBlocks=(total_lens+block_len-1)//block_len
        for block in range(numBlocks):
            response = data_pb2.Response(
                server_id=SERVER_ID)
            yield response
def serve():
    port = '50051'
    MAX_MESSAGE_LENGTH = 1000*1024*1024
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1),
                         options=[
               ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
               ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
               ("grpc.so_reuseport", 1),
               ("grpc.use_local_subchannel_pool", 1),
               ]
            )
    data_pb2_grpc.add_GRPCDemoServicer_to_server(DemoServer(), server)
    NEW_SERVICE_NAMES = (
        data_pb2.DESCRIPTOR.services_by_name['GRPCDemo'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(NEW_SERVICE_NAMES, server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


def main():
        NUM_WORKERS=5
        workers = []
        for _ in range(NUM_WORKERS):
            worker = multiprocessing.Process(target=serve)
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()

if __name__ == '__main__':
    logging.basicConfig()
    main()
