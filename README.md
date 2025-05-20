# Monitoramento Simulador API Python

Este repositório contém uma API simulada em Python com métricas exportadas no padrão Prometheus, permitindo o monitoramento de tráfego, latência, disponibilidade e uso de memória.

## 📦 Tecnologias utilizadas

- Python 3
- Flask
- Prometheus Client
- Docker
- Prometheus
- Grafana

## 🚀 Como executar a API localmente com Prometheus e Grafana

### Pré-requisitos

- Docker
- Docker Compose

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/monitoramento-simulador-api-python.git
cd monitoramento-simulador-api-python
```

### 2. Execute os containers

```bash
docker-compose up --build
```

### 3. Acesse os serviços

- API simulada: [http://localhost:5000](http://localhost:5000)
- Métricas Prometheus: [http://localhost:5000/metrics](http://localhost:5000/metrics)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)  
  (login padrão: `admin` / `admin`)

## 📊 Dashboard no Grafana

Para visualizar as métricas:

1. Acesse o Grafana em `http://localhost:3000`
2. Faça login com `admin / admin`
3. Adicione uma nova fonte de dados:
   - Tipo: Prometheus
   - URL: `http://prometheus:9090`
4. Crie um novo dashboard com os painéis desejados

## 📁 Estrutura do projeto

```
monitoramento-simulador-api-python/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── prometheus.yml
```

## 📌 Funcionalidades simuladas

- `/trafego` - Simula tráfego com latência
- `/disponibilidade` - Simula erro ocasional
- `/latencia` - Retorna tempos de resposta aleatórios
- `/memoria` - Simula uso crescente de memória
- `/metrics` - Endpoint de métricas para Prometheus

---

Este projeto é útil para testes de monitoramento, observabilidade e dashboards com Prometheus + Grafana em ambientes controlados.
