import grpc
import crawler_pb2
import crawler_pb2_grpc

# 定义连接 gRPC 服务器的函数
def run():
    # 连接服务器，此处地址为本地主机的 50051 端口
    # 在实际应用中，应替换为服务器的实际地址和端口
    with grpc.insecure_channel('localhost:60000') as channel:
        # 创建一个客户端对象
        stub = crawler_pb2_grpc.CrawlerStub(channel)

        # 创建一个 JsonRequest 请求对象
        request = crawler_pb2.JsonRequest(uid="329660103", dynamic_id="test", interruptible=False)

        # 调用服务端的 GetDynamicInfo 方法，并传入请求
        response = stub.GetDynamicInfo(request)

        # 打印响应内容
        print("客户端收到响应: ")
        print("code:", response.code)
        print("message:", response.message)
        print("data:", response.data)

if __name__ == '__main__':
    run()
