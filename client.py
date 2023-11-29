# 导入相关模块
import grpc
import hello_pb2
import hello_pb2_grpc

# 客户端运行函数
def run():
    # 创建到服务器的连接
    with grpc.insecure_channel('localhost:50051') as channel:
        # 创建一个stub（客户端对象），用于调用服务端方法
        stub = hello_pb2_grpc.GreeterStub(channel)

        # 调用SayHello方法，并传递HelloRequest消息
        response = stub.SayHello(hello_pb2.HelloRequest(name='world'))

        # 打印从服务端收到的消息
        print("Greeter client received: " + response.message)

# Python程序的入口点
if __name__ == '__main__':
    run()
