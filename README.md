# envoy_profile



## 代理

```shell
export https_proxy="http://127.0.0.1:1080"
export http_proxy="http://127.0.0.1:1080"
```

## 测试：

1. 启动grpc server:
    `make grpc_server`
2. 启动envoy:
    - 方式1.直接使用mac envoy:
        make envoy_mac
    - 方式2.使用docker envoy:
        make envoy_docker
3. 测试grpc直连:
    make grpc_client
4. 测试envoy 代理：
    make envoy_client


## iperf

```mermaid
flowchart LR
    MacClient[MacClient]-->|50Gbps|MacServer[MacServer:50051]
    MacClient[MacClient]-->|30Gbps|MacEnvoy[MacEnvoy:9911]-->MacServer[MacServer:50051]
    MacClient[MacClient]-->|400Mbps|DockerEnvoyClient[DockerEnvoyClient:9911]-->DockerEnvoyServer[DockerEnvoyServer:8811]-->MacServer[MacServer:50051]
    DockerClient[DockerClient]-->|1.8Gbps|MacServer[MacServer:50051]

    DockerComposeClient[DockerComposeClient]-->|24Gbps|DockerComposeServer[DockerComposeServer:50051]

```

## timeconsume[unary,streaming]
500次调用，每次发10MB，分别采用unary,streaming

```mermaid
flowchart LR
    MacClient[MacClient]-->|16.6s,17.5s|MacServer[MacServer:50051]
    MacClient[MacClient]-->|17.1s,17.3s|MacEnvoy[MacEnvoy:9911]-->MacServer[MacServer:50051]

    MacClient[MacClient]-->|>100s|DockerEnvoyClient[DockerEnvoyClient:9911]-->MacServer[MacServer:50051]

    DockerComposeClient[DockerComposeClient]-->|9.2s,10.5s|DockerComposeServer[DockerComposeServer:50051]



    DockerComposeClient[DockerComposeClient]-->|http2:11.8s,12.3s,http1:10.9s,12.1s|DockerComposeEnvoyClient[DockerComposeEnvoyClient]-->DockerComposeEnvoyServer[DockerComposeEnvoyServer]-->DockerComposeServer[DockerComposeServer:50051]
```
