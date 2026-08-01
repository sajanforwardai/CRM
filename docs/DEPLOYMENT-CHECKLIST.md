# Deployment Checklist — ForwardAI CRM

Use this before each production deploy to Render.

## Pre-Deployment (Local)

- [ ] All tests pass: `pnpm test`
- [ ] No TypeScript errors: `pnpm run type-check`
- [ ] No linting issues: `pnpm run lint`
- [ ] Database migrations are written: `apps/server/src/db/migrations/`
- [ ] Environment variables documented in `.env.example`
- [ ] API health endpoint working locally: `curl http://localhost:4000/api/health`
- [ ] Frontend loads locally: http://localhost:3000
- [ ] Git working tree is clean: `git status`

## Before Push to GitHub

- [ ] Commit message is clear and descriptive
- [ ] Feature branch is merged to `master`
- [ ] Code reviewed by at least one team member
- [ ] No secrets in code (check `.env.example` only)

## Render Auto-Deploy Steps

1. **Push to master:** `git push origin master`
2. **Render detects changes** (automatic)
3. **Services rebuild:**
   - Backend: ~2-3 min
   - Frontend: ~3-5 min
   - Database: N/A (schema only if migrations run)
4. **Monitor in Render dashboard:**
   - Check **Logs** for build errors
   - Verify **Metrics** (CPU/RAM healthy)
   - Test endpoints:
     - Backend: `curl https://forwardai-crm-api.onrender.com/api/health`
     - Frontend: Visit https://forwardai-crm-web.onrender.com

## Post-Deployment (Production)

- [ ] Frontend loads without errors (check browser console)
- [ ] Login flow works
- [ ] Can create a test client
- [ ] Can create a test project
- [ ] API responses are <500ms
- [ ] No 5xx errors in logs
- [ ] Slack notification sent to #engineering (if configured)

## Rollback (If Deploy Fails)

1. Go to Render service > **Deploys**
2. Find last working deploy
3. Click **Redeploy**
4. Verify health endpoints respond
5. Post incident summary (if needed)

## Database Migrations

Only database admin should run migrations:

```bash
# SSH into backend service
# In Render Shell:
cd apps/server && pnpm run db:migrate

# Verify migration status
pnpm run db:migrate --status
```

## Performance Monitoring

After deploy, check:
- **Render Metrics:** CPU, memory, network
- **Frontend Lighthouse:** Run `pnpm run build && pnpm run lighthouse` locally (target score ≥90)
- **API Response Times:** Check backend logs for slow queries

## Secrets Management

**Never commit secrets.** Use Render environment variables for:
- `JWT_SECRET`
- Database credentials (auto-managed by Render)
- API keys (future)

Rotate `JWT_SECRET` quarterly.
