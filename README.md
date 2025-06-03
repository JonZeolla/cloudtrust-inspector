# CloudTrust Inspector

CloudTrust Inspector is an open-source compliance management platform that helps security and platform teams track, verify, and report on AWS compliance posture. Built with modern technologies and designed for self-hosting, it provides a beautiful, intuitive interface for managing compliance controls, evidence, and reporting.

## Features

- 🎯 Modern, responsive React-based UI
- 🔒 AWS compliance control management
- 📊 Real-time compliance dashboards
- 📝 Evidence management and tracking
- 🤖 LLM-powered compliance assistance
- 📦 Custom control pack support
- 📤 Exportable compliance reports
- 🏗️ OSCAL-based data model
- 🚀 FastAPI backend for high performance
- 🔄 Real-time updates and notifications

## Tech Stack

- **Frontend**: React, TypeScript, Vite, TailwindCSS, Shadcn/ui
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL
- **Authentication**: OAuth2 with JWT
- **Container**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cloudtrust-inspector.git
   cd cloudtrust-inspector
   ```

2. Start the development environment:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

If you discover any security-related issues, please email security@cloudtrust-inspector.org instead of using the issue tracker. 