# browse-in-pages-crawler
Microservice of browse-in-pages

## gRPC generation command
```commandline
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello.proto
```

## TODO
- [ ] cookie 替换，查看有效期
- [ ] 放到 gRPC 流程中，给别人调用
- [ ] 打包成容器方便部署