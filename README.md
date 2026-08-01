# ForwardAI CRM

Customer Relationship Management platform for ForwardAI, an AI consulting firm. Manages clients, projects, team capacity, proposals, and revenue tracking.

## Stack

- **Frontend:** Next.js 14 (TypeScript, Tailwind CSS, shadcn/ui)
- **Backend:** Express.js (TypeScript, Drizzle ORM)
- **Database:** PostgreSQL
- **Deployment:** Render or VPS

## Getting Started

### Prerequisites
- Node.js 18+
- PostgreSQL 14+
- pnpm or npm

### Installation

```bash
# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local

# Run database migrations
pnpm run db:migrate

# Start development servers
pnpm run dev
```

Development runs on:
- Frontend: http://localhost:3000
- Backend API: http://localhost:4000

## Project Structure

- `apps/web/` — Next.js frontend dashboard
- `apps/server/` — Express.js backend API
- `docs/` — Specification and database schema
- `BRIEF.md` — Project brief and requirements

## Documentation

- [BRIEF.md](./BRIEF.md) — Complete project brief
- [spec.md](./docs/spec.md) — Technical specification (coming)
- [DATABASE.md](./docs/DATABASE.md) — Database schema reference (coming)

## License

Proprietary — ForwardAI
