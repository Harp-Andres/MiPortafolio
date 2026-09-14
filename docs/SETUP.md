# Setup & Installation Guide

## Prerequisites

- **Node.js**: v18+ (v24 recommended)
- **pnpm**: v12+
- **Git**: Latest version

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Harp-Andres/MiPortafolio.git
cd MiPortafolio
```

### 2. Install Dependencies
```bash
pnpm install
```

### 3. Install Python Dependencies (Optional - for backend)
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Development Environment Setup

### Frontend Development
```bash
# Start development server
pnpm -C apps/web dev

# Run tests
pnpm -C apps/web test

# Build for production
pnpm -C apps/web build
```

### Backend Development
```bash
# Start development server
pnpm -C apps/api dev

# Run tests
pnpm -C apps/api test
```

### Agent Development (Python)
```bash
cd agent
python -m venv venv
source venv/bin/activate
pip install -e .

# Run agent CLI
python -m agent.cli
```

## Environment Configuration

### Frontend (.env.local in apps/web)
```
VITE_API_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

### Backend (.env in apps/api)
```
DEBUG=True
DATABASE_URL=sqlite:///./test.db
CORS_ORIGINS=http://localhost:5173
```

### Agent (.env in agent/)
```
LOG_LEVEL=INFO
STORAGE_PATH=./data
```

## Monorepo Structure

```
MiPortafolio/
├── apps/
│   ├── web/                 # React frontend (Vite)
│   └── api/                 # Python FastAPI backend
├── packages/
│   ├── ui/                  # React UI components
│   ├── core/                # Shared utilities
│   ├── api-client/          # API client library
│   ├── backend/             # Backend utilities
│   └── config/              # Shared configuration
├── agent/                   # Python agent with 7-layer architecture
├── docs/                    # Documentation
└── scripts/                 # Automation scripts
```

## Troubleshooting

### Dependencies Not Installing
```bash
# Clear pnpm cache and reinstall
pnpm install --force
```

### Port Already in Use
```bash
# Change default ports in respective apps
# Frontend: vite.config.ts - server.port
# Backend: main.py - port parameter
# Agent: .env - AGENT_PORT
```

### Node Modules Issues
```bash
# Prune and reinstall
pnpm store prune
pnpm install
```

## Documentation Links

- [Architecture Overview](./MONOREPO_ARCHITECTURE.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [API Documentation](./API.md)
- [Agent Documentation](../agent/README.md)

## Support

For issues and questions:
1. Check [existing issues](https://github.com/Harp-Andres/MiPortafolio/issues)
2. Review development documentation in `.dev-docs/`
3. Contact the development team

## License

See LICENSE file in root directory
