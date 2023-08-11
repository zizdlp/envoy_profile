current_dir := $(shell pwd)
grpc_server:
	python grpc_service/server.py
grpc_client:
	python grpc_service/client.py --server=localhost:50051 --data_size=10 --times=500
envoy_mac:
	envoy -c envoy_mac/envoy.yaml
envoy_mac_convert:
	envoy -c envoy_mac/envoy_convert.yaml
envoy_mac_iperf:
	envoy -c envoy_mac/envoy_iperf.yaml
envoy_docker:
	docker run --rm -it \
		-v $(current_dir)/envoy_mac/envoy.yaml:/envoy.yaml \
		-p 8811:8811 \
		envoyproxy/envoy:dev-e2eaff90d31ead71af55f1535e819a6b382e1f68 \
			-c /envoy.yaml
envoy_docker_iperf:
	docker run --rm -it \
		-v $(current_dir)/envoy_mac/envoy_iperf.yaml:/envoy.yaml \
		-p 8811:8811 \
		envoyproxy/envoy:dev-e2eaff90d31ead71af55f1535e819a6b382e1f68 \
			-c /envoy.yaml
envoy_client:
	python grpc_service/client.py --server=localhost:8811 --data_size=10 --times=500
envoy_compose_client:
	python grpc_service/client.py --server=localhost:9911 --data_size=1 --times=500
docker_test:
	docker run --rm -it python bash
.PHONY: grpc_server grpc_client envoy_mac envoy_docker envoy_mac_iperf envoy_docker_iperf docker_test envoy_mac_convert envoy_compose_client


