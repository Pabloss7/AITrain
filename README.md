# AITrain: AI-Powered E-sports Performance Analysis

A microservices-based application designed to analyze **League of Legends** player performance using Artificial Intelligence. The system collects match data from Riot Games API, processes it through multiple specialized microservices, and generates personalized performance recommendations using Google's Gemma GenAI.

> [!WARNING]
> **Experimental Project**: This project is for educational and experimental purposes. It does not follow production best practices and is not optimized for high-scale environments.

---

## 🏗️ Architecture Overview

The project is built on a distributed microservices architecture, containerized with Docker:

```mermaid
    FE[ms-FE: Vite/React] --> CORE[ms-core: Spring Boot]
    CORE --> DC[ms-data-collector: Spring Boot]
    DC --> RIOT[Riot API]
    CORE --> PG[(Postgres)]
    DC --> AI[ms-ai: FastAPI/XGBoost]
    AI --> GEMMA [ms-gemma: FastAPI/GenAI]
    GEMMA --> HF[HuggingFace Hub]
    AI --> MONGO[(MongoDB)] 
    AI --> CORE
    CORE --> AI
    CORE --> FE
```

### 🛰️ Microservices Breakdown

| Service | Technology Stack | Responsibility |
| :--- | :--- | :--- |
| **ms-FE** | Vite, React, TypeScript | User dashboard and visualization of performance data. |
| **ms-core** | Java, Spring Boot, Postgres | Orchestration layer and user/session management. |
| **ms-data-collector**| Java, Spring Boot | Fetches and processes real-time match data from Riot API. |
| **ms-ai** | Python, FastAPI, XGBoost | ML service for match outcome prediction and metric analysis. |
| **ms-gemma** | Python, FastAPI, Gemma (LLM)| Generates natural language coaching advice based on stats. |

---

## 🚀 Getting Started

### 📋 Prerequisites

- **Docker & Docker Compose** installed.
- **NVIDIA GPU** (recommended for `ms-gemma`, requires [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)).
- **Riot Games API Key** ([Get it here](https://developer.riotgames.com/)).
- **HuggingFace Token**: Required to download and authenticate access to the gated **Gemma** model family. You must accept the model's terms on HuggingFace first.

### ⚙️ Configuration

1. Create a `.env` file in the root directory (you can copy `.env-complete` as a template).
2. Fill in the required environment variables:
   ```env
   RIOT_API_KEY=your_riot_api_key_here
   HF_TOKEN=your_huggingface_token_here
   ```

### 🛠️ Execution

To start the entire ecosystem, run:

```bash
docker-compose up -d --build
```

The services will be available at:
- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Core API**: [http://localhost:8181](http://localhost:8181)
- **AI Service**: [http://localhost:5000](http://localhost:5000)
- **Gemma Service**: [http://localhost:8000](http://localhost:8000)

---

## 📂 Project Structure

- `AI/`: Legacy AI research and XGBoost model training logic (microservice).
- `data/`:
    - `data_collector/`: Microservice for user-specific data retrieval.
    - `data_RIOT_collector/`: Scripts for batch data collection for training.
- `ms-FE/`: React-based frontend application.
- `ms-core/`: Main orchestration logic and data persistence. (entry point from frontend)
- `ms-gemma/`: GenAI service for recommendation generation.
- `compose.yaml`: Docker orchestration for the entire stack.

---

## 🧪 Development & Learning

This project serves as a learning environment for:
- Implementing a **Microservices Architecture**.
- Building **AI-integrated** applications.
- Managing **Dockerized** environments.
- Handling **Real-time Data** from third-party APIs (Riot Games).