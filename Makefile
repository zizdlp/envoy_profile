grpc_server:
	python grpc_service/server.py
grpc_client:
	python grpc_service/client.py --server=localhost:50051 --data_size=10 --times=500
envoy_mac:
	envoy -c envoy_mac/envoy.yaml
envoy_docker:
	bash envoy_proxy/run.sh
envoy_client:
	python grpc_service/client.py --server=localhost:8811 --data_size=10 --times=500
.PHONY: grpc_server grpc_client


