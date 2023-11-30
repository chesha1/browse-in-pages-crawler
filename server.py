from concurrent import futures
import grpc
import crawler_pb2
import crawler_pb2_grpc
import local_crawler


# 定义服务类，继承自生成的基类
class CrawlerService(crawler_pb2_grpc.CrawlerServicer):

    # 实现.proto文件中定义的RPC方法
    def GetDynamicInfo(self, request, context):
        a,b,c = request.uid,request.dynamic_id,request.interruptible
        code, message, data = local_crawler.get_dynamic_info_entrance(request.uid, request.dynamic_id,
                                                                      request.interruptible)

        # 构建响应消息
        return crawler_pb2.JsonResponse(
            code=code,
            message=message,
            data=data
        )


# 服务端启动函数
def serve():
    # 创建 gRPC 服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 将定义的服务类添加到 gRPC 服务器
    crawler_pb2_grpc.add_CrawlerServicer_to_server(CrawlerService(), server)

    # 指定服务器监听的端口
    server.add_insecure_port('[::]:60000')

    # 启动服务器
    server.start()
    # 服务器将一直运行，直到被中断或手动停止
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
