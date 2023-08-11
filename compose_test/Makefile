current_dir := $(shell pwd)
data_size := 10
times := 500
compose:
	bash run.sh
grpc_server:
	docker exec -it compose_test_grpc_server python grpc_service/server.py 
grpc_client:
	docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-server:50051 --data_size=$(data_size) --times=$(times)
envoy_client:
	docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-client-proxy:9911 --data_size=$(data_size) --times=$(times)
envoy_server:
	docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-server-proxy:8811 --data_size=$(data_size) --times=$(times)
envoy_client_http1:
	docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-client-proxy-http1:9911 --data_size=$(data_size) --times=$(times)
envoy_server_http1:
	docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-server-proxy-http1:8811 --data_size=$(data_size) --times=$(times)
local_grpc_server:
	python grpc_service/server.py
local_grpc_client:
	python grpc_service/client.py --server=localhost:50051 --data_size=$(data_size) --times=$(times)
envoy_mac:
	envoy -c ../envoy_mac/envoy.yaml
local_envoy_client:
	python grpc_service/client.py --server=localhost:8811 --data_size=$(data_size) --times=$(times)
.PHONY: compose grpc_client grpc_server envoy_client envoy_server local_grpc_server local_grpc_client local_envoy_client envoy_mac


