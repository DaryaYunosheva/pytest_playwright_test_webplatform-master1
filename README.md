# News Platform

Простая платформа для просмотра и создания новостей.

## Стек

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** React, TypeScript, Tailwind CSS, DaisyUI
- **Миграции:** Alembic

## Быстрый старт

### Docker

```bash
docker-compose up -d

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

Backend: http://localhost:8888

Frontend: http://localhost:5137

API Docs: http://localhost:8888/docs
