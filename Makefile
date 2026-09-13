.PHONY: up down logs test test-backend test-frontend seed reset demo dev-api dev-web

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

test: test-backend test-frontend

test-backend:
	python -m pytest -v

test-frontend:
	cd apps/web && npm test

seed:
	cd apps/api && python -m app.database.seed

reset:
	python -c "import httpx; print(httpx.post('http://localhost:8000/api/scenarios/reset').json())"

demo:
	python -c "import httpx; print(httpx.post('http://localhost:8000/api/demo/run').json())"

dev-api:
	python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir apps/api

dev-web:
	cd apps/web && npm run dev
