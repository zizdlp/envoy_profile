# FROM envoyproxy/envoy-dev:latest
FROM envoyproxy/envoy-dev:e2499c62a8f5983c31fdd20ee6dea43377e5b01e
COPY ./server/envoy-proxy.yaml /etc/server-envoy-proxy.yaml
RUN chmod go+r /etc/server-envoy-proxy.yaml
CMD ["/usr/local/bin/envoy", "-c", "/etc/server-envoy-proxy.yaml", "--service-cluster", "backend-proxy"]
