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
- [ ] 爬虫到指定位置停止
- [ ] 爬取评论区
- [ ] 触发反爬的异常处理

## 性能
为了躲过 B 站的反爬手段，每次 GET 之间有 1.5 秒的间隔，在这种情况下，`get_dynamic_info_list_with_interrupt` 和 `get_dynamic_info_list` 几乎没有性能区别

每个 item 有 6 个元素，爬取一个长度为 1282 的动态列表，用时 207 秒

## 部署
