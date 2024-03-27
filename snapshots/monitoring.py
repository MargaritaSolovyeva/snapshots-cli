import os

from prometheus_client import push_to_gateway, CollectorRegistry, Histogram
import time

registry = CollectorRegistry()

COMMAND_LATENCY = Histogram(
    'command_latency_seconds',
    'Command Latency',
    ['command'],
    registry=registry
)

gateway_host = os.getenv('PROMETHEUS_GATEWAY_URL')


def monitored(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        latency = end_time - start_time

        COMMAND_LATENCY.labels(func.__name__).observe(latency)
        push_to_gateway(gateway_host, job='shapshots', registry=registry)

        return result

    return wrapper

