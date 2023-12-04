# browse-in-pages-crawler
Microservice of browse-in-pages

## gRPC generation command
```commandline
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. crawler.proto
```

## TODO
- [ ] 打包成容器方便部署
- [ ] 设置爬取评论区超时返回
- [ ] 更新触发反爬的动态和评论爬取，把触发反爬的动态的id返回，作为新任务的开头
- [ ] 更新从某个开头开始的评论区爬取
- [ ] 重构可打断的动态爬取
- [ ] 访问发生错误'https://api.bilibili.com/x/v2/reply?oid=662016827293958168&type=17&sort=0&pn=506'
- [x] localhost的安全链接
- [ ] 远程安全链接
- [ ] Twitter（F12查找UserT）
- [ ] 微博
- [ ] type 11 的图片动态，id!=oid，需要一个新的入口

## 性能
为了躲过 B 站的反爬手段，每次 GET 之间有 2 秒的间隔，在这种情况下，`get_dynamic_info_list_with_interrupt` 和 `get_dynamic_info_list` 几乎没有性能区别

每个 item 有 6 个元素，爬取一个长度为 1282 的评论列表，用时 207 秒，这个过程中，都没有触发反爬

## 部署
