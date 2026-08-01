# Deployment Guide — ForwardAI CRM on Render

## Overview

ForwardAI CRM deploys to Render with three services:
- **forwardai-crm-db** — PostgreSQL database (managed)
- **forwardai-crm-api** — Express.js backend
- **forwardai-crm-web** — Next.js frontend

All services auto-redeploy on git push to `master` branch.

## Prerequisites

1. **Render account** — Sign up at https://render.com
2. **GitHub connected** — Link your GitHub account to Render
3. **Repository access** — Render needs access to `sajanforwardai/CRM`

## Initial Setup (First Deploy)

### 1. Connect GitHub to Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Select **"Public GitHub repository"**
4. Enter: `https://github.com/sajanforwardai/CRM`
5. Click **"Connect"**

### 2. Configure Blueprint Deployment

Render will read `render.yaml` and show three services ready to deploy:
- `forwardai-crm-db` (PostgreSQL)
- `forwardai-crm-api` (Express backend)
- `forwardai-crm-web` (Next.js frontend)

Review the plan (all Starter tier for MVP), then click **"Deploy"**.

**Deployment takes ~5-10 minutes.** Render will:
1. Provision the PostgreSQL database
2. Build and deploy the backend
3. Build and deploy the frontend

### 3. Set Environment Variables

Once deployed, go to each service's settings and add:

**Backend (forwardai-crm-api) > Environment**
- `JWT_SECRET` — Generate a strong random key (e.g., `openssl rand -base64 32`)
- Keep `DATABASE_URL`, `NODE_ENV`, `PORT` (Render auto-fills these)

**Frontend (forwardai-crm-web) > Environment**
- `NEXT_PUBLIC_API_URL` — Should be auto-filled as `https://forwardai-crm-api.onrender.com`
- `NEXT_PUBLIC_APP_URL` — Should be auto-filled as `https://forwardai-crm-web.onrender.com`

### 4. Run Database Migrations

Once the backend is live:

```bash
# SSH into the backend service and run migrations
curl -X POST https://forwardai-crm-api.onrender.com/api/db/migrate
```

Or manually via Render dashboard:
1. Go to **forwardai-crm-api** > **Shell**
2. Run: `cd apps/server && pnpm run db:migrate`

## Continuous Deployment

After initial setup, deployment is automatic:

1. **Push to GitHub:**
   ```bash
   git push origin master
   ```

2. **Render auto-detects changes** → rebuilds services → redeploys

3. **Monitor in Render dashboard:**
   - Logs: Each service has a live log viewer
   - Status: Green = healthy, Red = needs attention
   - Metrics: CPU, memory, bandwidth

## Service URLs

After successful deployment:

- **Frontend:** https://forwardai-crm-web.onrender.com
- **Backend API:** https://forwardai-crm-api.onrender.com
- **Database:** Managed internally (not publicly accessible)

## Custom Domain (Optional)

To use `crm.forwardai.dev`:

1. Go to **forwardai-crm-web** > **Settings** > **Custom Domain**
2. Add `crm.forwardai.dev`
3. Update DNS records (CNAME) to point to Render (Render provides exact value)
4. Wait for DNS propagation (~5-30 min)

Same process for backend API if desired.

## Scaling (After MVP)

When you need more power:

1. **Database:** Go to **forwardai-crm-db** > **Plan** → upgrade tier
2. **Backend/Frontend:** Go to service > **Plan** → upgrade from Starter to Standard ($12/mo)
3. **Auto-scaling:** Enable in service settings to scale with traffic

## Monitoring & Troubleshooting

### Check Service Status
- **Render dashboard:** All green = healthy
- **Logs:** Click service → **Logs** tab
- **Metrics:** CPU/Memory usage in **Metrics** tab

### Common Issues

**Backend not connecting to database:**
- Check `DATABASE_URL` env var is set correctly
- Verify migrations ran: `pnpm run db:migrate`
- Check backend logs for SQL errors

**Frontend not connecting to API:**
- Verify `NEXT_PUBLIC_API_URL` points to backend service
- Check browser console (F12) for CORS errors
- Verify backend health endpoint: `curl https://forwardai-crm-api.onrender.com/api/health`

**Slow deploys:**
- First deploy installs ~500 dependencies (slow but normal)
- Subsequent deploys are faster (cached dependencies)
- To speed up: ensure `.gitignore` excludes `node_modules/`, `.next/`, `dist/`

## Rollback

If a deployment breaks:

1. Go to service > **Deploys** tab
2. Find the last working deploy
3. Click **"Redeploy"**

Render keeps deploy history; rollback is instant.

## Cost

**Starter Plan (MVP):**
- Database: $15/month
- Backend: Free tier (512 MB RAM) or $7/month (Starter)
- Frontend: Free tier or $7/month (Starter)
- **Total: ~$22-29/month** (or free if using free tiers, with 15-min spin-up time)

Upgrade to Standard ($12-15/mo per service) for production reliability.

## Next: Local Development

While Render deploys backend + frontend, you'll also want local dev:

```bash
# Install dependencies
pnpm install

# Set up .env.local
cp .env.example .env.local
# Edit .env.local with local PostgreSQL URL

# Start dev servers (frontend + backend)
pnpm run dev
```

Frontend: http://localhost:3000
Backend: http://localhost:4000
