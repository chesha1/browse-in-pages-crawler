# 导入相关模块
from concurrent import futures
import grpc
import hello_pb2
import hello_pb2_grpc

# 定义服务类
class Greeter(hello_pb2_grpc.GreeterServicer):
    # 实现.proto文件中定义的SayHello方法
    def SayHello(self, request, context):
        # 返回一个HelloReply消息，其中包含问候语
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)

# 服务端运行函数
def serve():
    # 创建gRPC服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 将定义的服务类添加到gRPC服务器
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # 指定服务器监听的端口
    server.add_insecure_port('[::]:50051')

    # 启动服务器
    server.start()

    # 服务器等待终止信号
    server.wait_for_termination()

# Python程序的入口点
if __name__ == '__main__':
    serve()
