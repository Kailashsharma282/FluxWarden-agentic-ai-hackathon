# FluxWarden Production Deployment Guide (Render & Vercel)

This guide provides end-to-end instructions for deploying **FluxWarden** to production:
- **Backend API & Agent Engine**: Deployed on **Render** (Free Web Service)
- **Frontend Command Center**: Deployed on **Vercel** (Free Edge Network)

---

## Architecture Overview

```
                          ┌───────────────────────────┐
                          │   Vercel (Frontend)       │
                          │   https://fluxwarden.app   │
                          └─────────────┬─────────────┘
                                        │
                         REST API & WebSockets (/ws/events)
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   Render (FastAPI)        │
                          │   https://api.onrender.com│
                          └─────────────┬─────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
        ┌───────────────────────┐               ┌───────────────────────┐
        │  PostgreSQL / SQLite  │               │      LLM Engine       │
        │  (9 Relational Tables)│               │ Mock / Gemini / GPT-4o│
        └───────────────────────┘               └───────────────────────┘
```

---

## Part 1: Deploy Backend to Render

### Option A: 1-Click Blueprint Deploy (Using `render.yaml`)
1. Push your repository to GitHub.
2. Sign in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** ➔ **Blueprint**.
4. Select your `FluxWarden-Agentic-AI-Hackathon` GitHub repository.
5. Render reads `render.yaml` and automatically configures:
   - **Name**: `fluxwarden-api`
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `apps/api`
6. Click **Apply**. Render will build and deploy your API.
7. Copy your deployed API URL (e.g. `https://fluxwarden-api.onrender.com`).

### Option B: Manual Web Service Setup on Render
1. In Render Dashboard, click **New +** ➔ **Web Service**.
2. Connect your GitHub repository.
3. Configure the settings:
   - **Name**: `fluxwarden-api`
   - **Region**: Any (e.g. Oregon or Frankfurt)
   - **Branch**: `main`
   - **Root Directory**: `apps/api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
4. Under **Environment Variables**, add:
   | Key | Value | Notes |
   |---|---|---|
   | `PYTHON_VERSION` | `3.11.8` | Recommended Python version |
   | `LLM_PROVIDER` | `mock` *(or `gemini` / `openai`)* | Default zero-key mode |
   | `DATABASE_URL` | `sqlite+aiosqlite:///./fluxwarden.db` | Or connect Render Postgres |
   | `CORS_ORIGINS` | `*` | Permits Vercel frontend |
   | `GEMINI_API_KEY` | *(Optional)* | For Google Gemini live reasoning |
   | `OPENAI_API_KEY` | *(Optional)* | For OpenAI GPT-4o live reasoning |
5. Click **Deploy Web Service**.
6. Note the public URL: `https://<YOUR_RENDER_SERVICE>.onrender.com`.

---

## Part 2: Deploy Frontend to Vercel

### Step-by-Step Vercel Setup:
1. Sign in to [Vercel Dashboard](https://vercel.com/).
2. Click **Add New...** ➔ **Project**.
3. Import your `FluxWarden-Agentic-AI-Hackathon` repository.
4. In the project configuration modal:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click **Edit** and select `apps/web`.
5. Under **Environment Variables**, add:
   | Key | Value | Notes |
   |---|---|---|
   | `VITE_API_URL` | `https://<YOUR_RENDER_SERVICE>.onrender.com` | Your Render backend URL |
6. Click **Deploy**.
7. Vercel will run `npm install`, compile 1,894 modules in ~20 seconds, and deploy to a global URL (e.g., `https://fluxwarden.vercel.app`).

---

## Part 3: Adding Real API Keys (Google Gemini / OpenAI)

You can add or switch API keys in **two ways**:

### Method 1: In the Live Command Center UI (Instant)
1. Open your deployed Vercel frontend in the browser.
2. In the top navigation bar, click **Settings**.
3. Under **Cognitive Provider Abstraction**, select **GEMINI** or **OPENAI**.
4. Paste your API key:
   - **Gemini**: Obtain free at [Google AI Studio](https://aistudio.google.com/app/apikey).
   - **OpenAI**: Obtain at [OpenAI API Keys](https://platform.openai.com/api-keys).
5. Click **Apply Configuration**.
6. The backend immediately activates the real LLM engine without needing a server restart!

### Method 2: In Render Environment Variables
1. In Render Dashboard ➔ `fluxwarden-api` ➔ **Environment**.
2. Add:
   - `LLM_PROVIDER=gemini` (or `openai`)
   - `GEMINI_API_KEY=AIzaSy...` (or `OPENAI_API_KEY=sk-...`)
3. Click **Save Changes**. Render will perform a zero-downtime rolling restart.

---

## Part 4: How to Verify Cloud Deployment

1. **Verify Backend**:
   Visit `https://<YOUR_RENDER_SERVICE>.onrender.com/health` in your browser.
   Response should be:
   ```json
   { "status": "healthy", "timestamp": 1789324800.0 }
   ```

2. **Verify Interactive API Docs**:
   Visit `https://<YOUR_RENDER_SERVICE>.onrender.com/docs` to test interactive Swagger endpoints.

3. **Verify Frontend**:
   Open `https://<YOUR_VERCEL_APP>.vercel.app/`.
   - Click **Launch Command Center**.
   - Check the **WebSocket Status Indicator** in the header (glowing green dot).
   - Click **RUN DEMO** to observe the full 15-step adaptive incident resolution live on cloud infrastructure!
