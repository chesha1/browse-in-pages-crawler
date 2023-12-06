# browse-in-pages-crawler
Microservice of browse-in-pages

## gRPC generation command
```commandline
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. crawler.proto
```

## TODO
- [ ] 设置爬取评论区超时返回
- [ ] 更新触发反爬的动态和评论爬取，把触发反爬的动态的id返回，作为新任务的开头
- [ ] 更新从某个开头开始的评论区爬取
- [ ] 访问发生错误'https://api.bilibili.com/x/v2/reply?oid=662016827293958168&type=17&sort=0&pn=506'
- [ ] Twitter（F12查找UserT）
- [ ] 微博
- [ ] type 11 的图片动态，id!=oid，需要一个新的入口
- [ ] type 1 的视频，错误返回

## 性能
为了躲过 B 站的反爬手段，每次 GET 之间有 2 秒的间隔，在这种情况下，`get_dynamic_info_list_with_interrupt` 和 `get_dynamic_info_list` 几乎没有性能区别

每个 item 有 8 个元素，爬取一个长度为 1200 的用户的动态列表，用时 251.4 秒，这个过程中，都没有触发反爬

每个 item 有 6 个元素，爬取一个长度为 826 的动态的评论列表，用时 98.8 秒，这个过程中，都没有触发反爬

## 安全连接
生成一个为运行在特定 IP 地址（如 106.15.44.72）的微服务使用的证书，需要完整地遵循以下步骤：

### 1. 安装 OpenSSL

确保您的系统已安装 OpenSSL。

### 2. 生成根证书（CA）

#### a. 创建根密钥

```bash
openssl genrsa -out ca.key 2048
```

#### b. 创建并自签名根证书

```bash
openssl req -new -x509 -days 36500 -key ca.key -out ca.crt -subj "/CN=My Root CA"
```

### 3. 创建服务器证书

#### a. 生成服务器私钥

```bash
openssl genrsa -out server.key 2048
```

#### b. 创建 OpenSSL 配置文件

创建一个新的配置文件 `san.cnf` 包含以下内容：

```ini
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[dn]
CN = localhost

[req_ext]
subjectAltName = @alt_names

[alt_names]
IP.1 = 106.15.44.72
```

#### c. 创建证书签名请求（CSR）

使用新的配置文件创建 CSR：

```bash
openssl req -new -key server.key -out server.csr -config san.cnf
```

#### d. 使用根证书签发服务器证书

```bash
openssl x509 -req -days 36500 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt -extensions req_ext -extfile san.cnf
```

### 4. 验证证书

```bash
openssl verify -CAfile ca.crt server.crt
```

这个命令用来验证服务器证书是否有效。

### 5. 使用证书配置 gRPC

在 gRPC 服务器和客户端上使用生成的 `server.crt` 和 `server.key`。配置方式会根据你使用的编程语言和 gRPC 库有所不同。

请注意，这些步骤生成的证书仅适用于开发和测试环境。在生产环境中，应使用由受信任的证书颁发机构（CA）签发的证书。
## 部署
1. `git clone` 本仓库，注意本仓库不包含证书文件
2. 构建镜像
    ```commandline
    docker build -t crawler .
    ```
3. 运行容器
    ```commandline
    docker run -d -p 60000:60000 crawler
    ```

