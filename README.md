# Microservices and AI-based App for E-sports Performance Analysis

⚠️ **Disclaimer**: This project **does not follow best development practices** and is **not optimized for production**. Its main purpose is to **learn and experiment** as part of my Final Degree Project (TFG) in Computer Engineering.  

The project is a **microservices-based application using Artificial Intelligence** to analyze E-sports player performance, specifically for **League of Legends**. It collects match data, processes it, generates performance metrics, and predicts outcomes using AI models.

---

## Project Structure

AITRAIN/
│
├── AI/ # Contains AI microservice
│ ├── xgboostModel.py
│ ├── fastapi_server.py
│ └── ... # Other scripts related to explainers and data
│
├── data/ # Data related
│ ├── data_collector/ # java-springboot ms for obtaining the data from the users from riot
│ ├── data_RIOT_collector / # java script for obtaining massive data to train AI from RIOT
│ └── data_preparation/ # Scripts for preparing the data for the AI model
├── Frontend/ # User interface (not yet)
│ └── ...

## Tools and Technologies Used

- **Python** 🐍 (for AI and data analysis)  
- **XGBoost** ⚡ (prediction model)  
- **Java / Spring Boot** ☕ (REST API)  
- **Docker** 🐳 (containerization)  
- **PostgreSQL / MongoDB** 🗄️ (databases)  

---

This project is **experimental and educational**, serving primarily as a **learning environment** to understand microservices, AI pipelines, and E-sports performance analysis.