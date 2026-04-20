# 🗺️ SmartTourism City Guide

**The intelligent tourism guide platform combining real-time data, AI recommendations, and human connections.**

![Version](https://img.shields.io/badge/version-0.1.0-beta)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-In%20Development-orange)

---

## 🎯 What is SmartTourism?

A **complete smart city tourism ecosystem** for A Coruña that:

- 🗺️ Shows real-time POI availability with occupancy levels
- 🧠 Learns user preferences and recommends personalized itineraries
- 🤝 Connects travelers with similar interests
- 📊 Provides city managers with visitor flow analytics
- 💬 Offers a conversational AI guide in multiple languages
- 🎨 Visualizes the city in 3D with live movement data

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/pablorubal/SmartTourism-City-Guide.git
cd SmartTourism-City-Guide

# Install dependencies
make install

# Setup environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start development environment
make dev

# Or use Docker
make docker-up
```

### Endpoints
- Backend API: http://localhost:8000
- Frontend PWA: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## 🏗️ Architecture

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI, Pydantic | REST API & orchestration |
| **Frontend** | React, Vite, Leaflet | Web PWA |
| **Context** | Orion CB (NGSI-LD) | Real-time data broker |
| **TimeSeries** | QuantumLeap, TimescaleDB | Behavior history |
| **ML** | scikit-learn | Recommendations & matching |
| **Geospatial** | GeoPandas | Route optimization |
| **3D** | Three.js | City visualization |
| **Chat** | Ollama, Llama 3 | Local LLM guide |
| **Frontend Cache** | PWA Service Workers | Offline capability |

### Folder Structure

```
SmartTourism-City-Guide/
├── backend/           → FastAPI application
├── frontend/          → React + Vite PWA
├── ml-engine/         → Recommendation & matching models
├── docs/              → Architecture & API documentation
├── config/            → Docker & environment configs
└── README.md          → This file
```

---

## 🧬 Core Entities (NGSI-LD)

- **TouristProfile** - User preferences, interests, mobility
- **TouristTrip** - Active itinerary with real visits
- **TouristDestination** - City metadata (A Coruña)
- **PointOfInterest** - POI coordinates, ratings, occupancy
- **Museum**, **Beach**, **Event**, **TouristRental** - Specialized POI types
- **ConsumptionBehavior** - Time spent, money, visit sequences
- **SocialMatch** - Traveler affinities and suggested meetings
- **Alert** - Real-time notifications
- **Device** - IoT sensors (cameras, beacons, QR/NFC)

---

## 🎯 Features

### F1 — Smart City Map
- Interactive Leaflet map with real-time POI updates
- Occupancy semaphore (🟢 available, 🟡 >70%, 🔴 full/closed)
- Personal affinity scores for each POI
- WebSocket updates < 10s latency

### F2 — Recommendation Engine
- ML-powered route optimization
- Considers distance, hours, occupancy, user profile
- Dynamic adjustment based on real behavior

### F3 — Management Dashboard
- Grafana analytics for city officials
- Visitor flow heatmaps
- Nationality analysis, dwell times
- Saturation detection

### F4 — 3D City Visualization
- Three.js reconstruction of A Coruña
- Buildings respond to live occupancy
- Animated particle flow of visitors

### F5 — Conversational Guide
- Local LLM (Ollama + Llama 3)
- Natural language queries
- Multi-language support

### F6 — Social Travel Match
- Algorithm detects traveler affinities
- Suggests shared visits
- AI-powered icebreaker conversations

---

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design & data flow
- [Entities](docs/ENTITIES.md) - Complete NGSI-LD specification
- [API](docs/API.md) - REST endpoints & examples
- [Setup](docs/SETUP.md) - Detailed environment configuration

---

## 🤝 Contributing

We follow **GitHub Flow** for all contributions.

**Workflow:**
1. Create a new branch from `main`
2. Make your changes
3. Commit with clear messages referencing issues
4. Push branch and create a Pull Request
5. Maintainers review and merge to `main`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🧪 Testing

```bash
# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm test

# Lint & format
make lint
```

---

## 🐳 Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Orion CB (port 1026)
- TimescaleDB (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 5173)

---

## 📊 Roadmap

- ✅ Project structure
- 🚀 Smart map (F1)
- 🚀 Recommendation engine (F2)
- 🚀 Management dashboard (F3)
- 🚀 3D city (F4)
- 🚀 Chat guide (F5)
- 🚀 Social matching (F6)
- 🚀 Mobile optimization
- 🚀 Analytics platform

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👋 Authors

- **Pablo Rubal** - Initial development

---

## 🙏 Acknowledgments

- A Coruña city council
- FIWARE community (NGSI-LD standards)
- Open-source contributors

---

**Made with ❤️ for travelers, developers, and cities.**

For questions or issues, [create an issue](https://github.com/pablorubal/SmartTourism-City-Guide/issues) on GitHub.
