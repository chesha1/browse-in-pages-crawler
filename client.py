import json

import grpc
import crawler_pb2
import crawler_pb2_grpc


# 定义连接 gRPC 服务器的函数
def run():
    # 读取服务器证书
    with open('server.crt', 'rb') as f:
        trusted_certs = f.read()

    # 创建SSL凭证
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    # 在实际应用中，应替换为服务器的实际地址和端口
    with grpc.secure_channel('106.15.44.72:60000', credentials) as channel:
    # with grpc.secure_channel('localhost:60000', credentials) as channel:
        # 创建一个客户端对象
        stub = crawler_pb2_grpc.BiliCrawlerStub(channel)

        # 创建一个 Request 请求对象
        request = crawler_pb2.BiliDynamicRequest(uid="329660103", dynamic_id="test", interruptible=False)

        # 调用服务端的 GetDynamicInfo 方法，并传入请求
        response = stub.GetDynamicInfo(request)
        data = response.data
        data_obj = json.loads(data)
        # 打印响应内容
        print("客户端收到响应: ")
        print("code:", response.code)
        print("message:", response.message)
        print("data:", data)


if __name__ == '__main__':
    run()
