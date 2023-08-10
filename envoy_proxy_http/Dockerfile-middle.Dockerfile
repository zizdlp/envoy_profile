# FROM envoyproxy/envoy-dev:latest
FROM envoyproxy/envoy-dev:e2499c62a8f5983c31fdd20ee6dea43377e5b01e
COPY ./middle/envoy-proxy.yaml /etc/middle-envoy-proxy.yaml
RUN chmod go+r /etc/middle-envoy-proxy.yaml
CMD ["/usr/local/bin/envoy", "-c", "/etc/middle-envoy-proxy.yaml"]
