# 🚀 AI-Driven Multidimensional Trust Management for Distributed Edge Nodes using Project Alvarium

An AI-driven multidimensional trust management framework for distributed edge computing environments inspired by **Project Alvarium**. The framework continuously monitors edge node performance, computes multidimensional trust scores, predicts future trust degradation using a Transformer-based AI model, and visualizes trust metrics through a real-time dashboard.

---

## 📖 Overview

Distributed edge computing environments consist of multiple heterogeneous edge nodes that continuously process data closer to end users. Ensuring the reliability and trustworthiness of these nodes is challenging due to dynamic workloads, varying network conditions, and resource constraints.

This project introduces an intelligent trust management framework that:

- Collects real-time metrics from distributed edge nodes.
- Computes multidimensional trust scores.
- Predicts future trust degradation using AI.
- Stores trust annotations inspired by Project Alvarium.
- Provides real-time monitoring through an interactive dashboard.
- Supports scalable deployment using Docker and Kubernetes.

---

## 🏗 System Architecture

The framework consists of the following components:

- Edge Nodes
- FastAPI Gateway
- Redis Database
- Trust Collector
- Trust Analyzer
- Trust Engine
- Transformer-Based AI Trust Predictor
- Streamlit Dashboard
- Kubernetes Cluster

---

## ✨ Features

- Real-time edge node monitoring
- Multidimensional trust computation
- Operational Trust
- Resource Trust
- Network Trust
- Data Trust
- Historical Trust
- AI-based trust prediction using Transformer
- Real-time visualization dashboard
- Redis-based annotation storage
- Docker containerization
- Kubernetes orchestration
- Project Alvarium-inspired confidence annotations

---

## 🧠 Trust Computation

The overall trust score is computed using five trust dimensions:

- **Operational Trust**
  - Success Rate
  - Availability
  - Uptime

- **Resource Trust**
  - CPU Utilization
  - Memory Utilization

- **Network Trust**
  - Latency

- **Data Trust**
  - Success Rate

- **Historical Trust**
  - Average of previous trust dimensions

The final trust score is calculated as

```
Trust =
0.30 × Operational Trust
+ 0.25 × Resource Trust
+ 0.20 × Network Trust
+ 0.15 × Data Trust
+ 0.10 × Historical Trust
```

---

## 🤖 AI Trust Prediction

Historical trust values are analyzed using a **Transformer-based AI model** to learn temporal dependencies and forecast future trust degradation.

This enables:

- Early identification of unreliable nodes
- Predictive trust analytics
- Trust-aware decision making

---

## 📊 Dashboard

The Streamlit dashboard provides:

- Live trust score monitoring
- Edge node selection
- Latency visualization
- CPU utilization
- Memory utilization
- Availability
- Historical trust trends
- Trust status classification

---

## 🛠 Tech Stack

### Programming Language

- Python 3.11

### Backend

- FastAPI

### Database

- Redis

### AI/ML

- PyTorch
- Transformer Model

### Dashboard

- Streamlit
- Matplotlib
- Pandas

### Containerization

- Docker

### Orchestration

- Kubernetes (KIND)

### Communication

- REST APIs

---

## 📂 Project Structure

```
.
├── api/
│   ├── main.py
│   └── requirements.txt
│
├── sender/
│   └── real_metrics_sender.py
│
├── worker/
│   ├── trust_engine.py
│   ├── transformer_model.py
│   └── worker.py
│
├── dashboard/
│   └── dashboard.py
│
├── kubernetes/
│   ├── api.yaml
│   ├── redis.yaml
│   ├── sender.yaml
│   ├── worker.yaml
│   └── edge-service.yaml
│
├── Dockerfiles/
│
├── report/
│
└── README.md
```

---

## 🚀 Running the Project

### Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Driven-Multidimensional-Trust-Management.git

cd AI-Driven-Multidimensional-Trust-Management
```

---

### Build Docker Images

```bash
docker build -t trust-api .
docker build -t trust-worker .
docker build -t trust-sender .
```

---

### Deploy Kubernetes Resources

```bash
kubectl apply -f kubernetes/
```

---

### Port Forward Redis

```bash
kubectl port-forward svc/redis-service 6380:6379
```

---

### Run Dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

## 📈 Experimental Evaluation

The framework was evaluated on a Kubernetes cluster with multiple simulated edge nodes.

The evaluation demonstrates:

- Dynamic trust computation
- Real-time metric collection
- AI-driven trust prediction
- Fault-tolerant deployment
- Continuous trust monitoring

---

## 📄 Research Paper

The complete IEEE research paper describing the methodology, implementation, and experimental evaluation is included in this repository.

---

## 🔮 Future Work

- Federated Learning-based trust prediction
- Blockchain-enabled trust verification
- Adaptive trust weighting
- Support for heterogeneous edge environments
- Integration with real IoT edge devices

---

## 👩‍💻 Authors

- Sneha S. Baragi
- Aparna Shegade
- Bhagyashree A. Mugalkhod
- Sahana R. Ghulannavar
- Pooja Shettar

Department of Computer Science and Engineering (AI)

KLE Technological University, Hubballi, India

---

## 📜 License

This project is developed for academic and research purposes.