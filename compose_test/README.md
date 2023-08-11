# run compose
bash run.sh

# run grpc server
docker exec -it compose_test_grpc_server python grpc_service/server.py 

# run grpc client
docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-server:50051 --data_size=1 --times=500

# run envoy client
docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-client-proxy:9911 --data_size=1 --times=500

# run envoy server
docker exec -it compose_test_grpc_server python grpc_service/client.py  --server=grpc-server-proxy:8811 --data_size=1 --times=500