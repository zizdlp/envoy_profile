# 使用iperf 进行性能测试

# 带宽测试

1. server:
iperf -s -p 50051

2. test:
    1. 测试直连：
      iperf -c 192.168.112.9 -p 50051
    2. 测试通过envoy_mac_iperf:
      iperf -c 192.168.112.9 -p 8811 
    3. 测试通过envoy_docker_iperf:
      iperf -c 192.168.112.9 -p 8811 

3. test docker:



#### 测试结果

1. mac 本地不进行端口转发：50G+bps
2. mac 本地进行envoy转发: 30G+bps
3. mac 使用docker envoy转发:400+Mbps
4. mac 使用docker，docker内测测试：1.8Gbps