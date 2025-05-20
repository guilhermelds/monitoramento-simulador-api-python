from functools import wraps
from flask import Flask, request, jsonify, make_response
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import threading
import time
import random
import requests
import psutil

app = Flask(__name__)

# Métricas Prometheus com label status_code
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP Errors (status >= 400)', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency', ['endpoint'])
CPU_USAGE = Gauge('simulated_cpu_usage_percent', 'Simulated CPU usage')
MEMORY_USAGE = Gauge('simulated_memory_usage_mb', 'Simulated memory usage in MB')

# Informações da máquina
TOTAL_MEMORY = psutil.virtual_memory().total / (1024 * 1024)  # em MB

# Função de carga aleatória
def simulate_load():
    while True:
        cpu_target = random.uniform(0.0, 0.5) * 100  # até 50% da CPU
        mem_target = random.uniform(0.0, 0.5) * TOTAL_MEMORY  # até 50% da memória

        # Simula CPU: loop pesado por tempo aleatório
        if random.random() < 0.7:
            duration = random.uniform(0.1, 1.5)
            start = time.time()
            while time.time() - start < duration:
                _ = [x**2 for x in range(1000)]

        CPU_USAGE.set(cpu_target)
        MEMORY_USAGE.set(mem_target)

        time.sleep(random.uniform(0.5, 2.0))

# Função de rajadas de tráfego (requisições internas)
def simulate_traffic():
    endpoints = ['/', '/status', '/random']
    while True:
        if random.random() < 0.3:
            num_requests = random.randint(1, 5)
        else:
            num_requests = random.randint(10, 100)  # pico

        for _ in range(num_requests):
            try:
                requests.get(f'http://localhost:5000{random.choice(endpoints)}', timeout=1)
            except:
                pass
            time.sleep(random.uniform(0.01, 0.2))
        time.sleep(random.uniform(1, 5))

# Função auxiliar para escolher status aleatório
def random_status():
    # 80% chance 200, 10% chance 400, 10% chance 500
    return random.choices([200, 400, 500], weights=[0.8, 0.1, 0.1])[0]

# Decorador para medir latência e contar requisições com status_code
def track_metrics(endpoint):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with REQUEST_LATENCY.labels(endpoint).time():
                response = func(*args, **kwargs)
                status_code = getattr(response, "status_code", 200)
                REQUEST_COUNT.labels(request.method, endpoint, str(status_code)).inc()
                if status_code >= 400:
                    ERROR_COUNT.labels(request.method, endpoint, str(status_code)).inc()
                return response
        return wrapper
    return decorator

# Rotas simuladas com status code aleatório

@app.route('/')
@track_metrics('/')
def home():
    delay = random.uniform(0.01, 1.5)
    time.sleep(delay)
    status = random_status()
    response = make_response("Hello from the chaotic API!", status)
    return response

@app.route('/status')
@track_metrics('/status')
def status():
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)
    status = random_status()
    response = make_response(jsonify({"status": "ok"}), status)
    return response

@app.route('/random')
@track_metrics('/random')
def random_stuff():
    delay = random.uniform(0.2, 3.0)
    time.sleep(delay)
    value = random.randint(0, 1000)
    status = random_status()
    response = make_response(jsonify({"value": value}), status)
    return response

# Inicialização
if __name__ == '__main__':
    start_http_server(8000)  # Endpoint Prometheus: http://localhost:8000/metrics

    threading.Thread(target=simulate_load, daemon=True).start()
    threading.Thread(target=simulate_traffic, daemon=True).start()

    app.run(host='0.0.0.0', port=5000)
