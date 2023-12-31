from concurrent import futures
import grpc
import crawler_pb2
import crawler_pb2_grpc
import local_crawler


# 定义服务类，继承自生成的基类
class BiliCrawlerService(crawler_pb2_grpc.BiliCrawlerServicer):

    # 实现.proto文件中定义的RPC方法
    def GetDynamicInfo(self, request, context):
        code, message, data = local_crawler.bili_get_dynamic_info_list(request.uid, request.dynamic_id,
                                                                       request.interruptible)

        # 构建响应消息
        return crawler_pb2.BiliDynamicResponse(
            code=code,
            message=message,
            data=data
        )

    def GetCommentInfo(self, request, context):
        return None


# 服务端启动函数
def serve():
    # 创建 gRPC 服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 将定义的服务类添加到 gRPC 服务器
    crawler_pb2_grpc.add_BiliCrawlerServicer_to_server(BiliCrawlerService(), server)

    # 读取证书和密钥
    with open('server.crt', 'rb') as f:
        certificate_chain = f.read()
    with open('server.key', 'rb') as f:
        private_key = f.read()

    # 创建SSL凭证
    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)])

    # 指定服务器监听的端口
    server.add_secure_port('0.0.0.0:60000', server_credentials)

    # 启动服务器
    server.start()
    # 服务器将一直运行，直到被中断或手动停止
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
