# Swarm Brief: ForwardAI Consulting CRM

## Project Context
ForwardAI is an AI consulting firm that builds intelligent systems for financial services, advising wealth managers, portfolio managers, and enterprise clients. This CRM tracks all client relationships, projects, team capacity, and revenue. It will be deployed at `forwardai.dev/crm` and serve as the operational backbone for proposal management, project timelines, and client engagement.

**Stack:**
- Frontend: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- Backend: Node.js + Express, TypeScript, PostgreSQL
- GitHub repo: `sajanforwardai/CRM`
- Deployment: Render or VPS (via `/workspace/.swarm/praxis/toolkit/`)

## Your Mission
Build the **MVP1 Foundation**: Client management, project tracking, proposal workflow, and team capacity dashboard. This is the core operational system ForwardAI uses daily.

## What To Build

### 1. Data Model & Schema
**Core entities** (PostgreSQL):
- `clients` — company name, industry, contact person, engagement type (retainer/project), annual_value, status (prospect/active/closed)
- `projects` — client_id, title, description, status (proposal/active/completed), start_date, end_date, estimated_hours, actual_hours
- `proposals` — project_id, status (draft/sent/won/lost), value, created_at, sent_date, closed_date
- `team_members` — name, role, billable_rate, capacity_hours_per_week, current_allocation
- `allocations` — team_member_id, project_id, hours_per_week, start_date, end_date
- `deliverables` — project_id, title, status (pending/in_progress/completed), due_date, owner_id
- `invoices` — project_id, amount, status (draft/sent/paid), due_date

**Relationships:** One client has many projects. One project has many team allocations. Team members allocate time across multiple projects.

### 2. Dashboard (Authenticated Home)
- **KPIs section (top):** Total pipeline value, active projects count, team utilization %, revenue YTD
- **Client list:** Table with company name, primary contact, last engagement, status, annual value. Sortable, filterable by status.
- **Active projects timeline:** Gantt-style or card view showing project phase, team assigned, days remaining.
- **Team capacity widget:** Simple bar chart — hours allocated vs. available this week. Red if over-allocated.
- **Recent activity feed:** Last proposals sent, projects started, deliverables completed.

### 3. Client Management (`/clients`)
- **List view:** All clients in a table (company, contact, status, annual value, last project date). Sortable, filterable, searchable.
- **Add Client form:** Company name, industry dropdown, primary contact email/phone, engagement type, expected annual value.
- **Client detail page** (`/clients/[id]`):
  - Overview card: contact info, engagement type, total spend, projects count
  - Projects tab: all projects for this client
  - Proposals tab: all proposals (status, value, dates)
  - Activity tab: timeline of all interactions (proposals sent, projects started, completed)
  - Edit button (name, contact, annual value, status)

### 4. Project Management (`/projects`)
- **List view:** All projects, columns: client name, project title, status, team size, hours allocated/estimated, progress %. Filterable by status (proposal/active/completed).
- **Create project form:** Client name, title, description, start date, estimated hours, status.
- **Project detail page** (`/projects/[id]`):
  - **Overview:** Client, status, dates, estimated vs. actual hours, progress bar
  - **Deliverables:** List of deliverables for the project, checkbox to mark complete
  - **Team:** Table of assigned team members, hours per week, role
  - **Financials:** Estimated revenue, actual cost (team hours × rate), margin
  - **Timeline:** Gantt or milestones view
  - **Edit** and **Archive** buttons

### 5. Proposal Workflow (`/proposals`)
- **List view:** All proposals, columns: client, project title, value, status (draft/sent/won/lost), created date, due date.
- **Create proposal form:**
  - Auto-fill: client name, project scope from draft project
  - Fields: title, description, scope of work, deliverables, timeline, team (proposed), rate/value, terms, due date
  - **Draft mode:** Save as draft, preview, send
- **Proposal detail page** (`/proposals/[id]`):
  - Read-only or edit view (if draft)
  - Show status timeline: created → sent → won/lost, with dates
  - **Send proposal** button (marks sent_date, changes status to "sent")
  - **Mark Won/Lost** button (closes proposal, updates project status)
  - **Edit** link (if draft)

### 6. Team & Capacity (`/team`)
- **Team list:** Table with name, role, billable rate, hours available per week, current utilization %.
- **Add team member form:** Name, role dropdown (consultant/senior/principal), billable rate, capacity hours/week.
- **Team member detail page** (`/team/[id]`):
  - Basic info (name, role, rate, total capacity)
  - **Current allocations:** List of active projects, hours per week, end date
  - **Utilization chart:** Bar chart, hours allocated vs. available for next 4 weeks
  - **Historical:** Total hours billed this month, this quarter
  - **Edit/Archive** buttons

### 7. Authentication & Authorization
- **Login:** Email/password (no OAuth for MVP)
- **Roles:** Admin (full access), Manager (view all, create/edit projects/proposals), Team (view own allocations + assigned projects only)
- Session stored in JWT token, httpOnly cookie
- Protected routes: `/clients`, `/projects`, `/proposals`, `/team`, `/dashboard` require login
- Role-based UI: Only admins see "Add Team Member", only managers can send proposals

### 8. Reports & Exports (Future but structure for it)
- Clients & pipeline value summary (CSV export)
- Project profitability (hours vs. revenue)
- Team utilization report

## Technical Constraints
- **Backend:** Express.js + TypeScript, Drizzle ORM (type-safe SQL), PostgreSQL
- **Frontend:** Next.js 14 App Router, Server Components by default
- **Auth:** JWT in httpOnly cookies, bcrypt password hashing
- **UI:** shadcn/ui for components, Tailwind CSS for styling
- **Data validation:** Zod schemas (backend input + frontend types)
- **No hardcoded data** — all from database
- Database migrations via Drizzle migrations (version controlled)
- API responses: typed with Zod (ensures frontend knows schema)

## File Structure Target
```
sajanforwardai/CRM/
├── .github/workflows/
│   ├── test.yml
│   └── deploy.yml
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx        # Dashboard (after login)
│   │   │   ├── login/page.tsx
│   │   │   ├── (protected)/
│   │   │   │   ├── layout.tsx  # Auth guard + sidebar
│   │   │   │   ├── clients/
│   │   │   │   ├── projects/
│   │   │   │   ├── proposals/
│   │   │   │   └── team/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── client/
│   │   │   ├── project/
│   │   │   ├── proposal/
│   │   │   └── shared/
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── utils.ts
│   │   └── middleware.ts       # Auth guard
│   └── server/                 # Express backend
│       ├── src/
│       │   ├── index.ts
│       │   ├── routes/
│       │   │   ├── auth.ts
│       │   │   ├── clients.ts
│       │   │   ├── projects.ts
│       │   │   ├── proposals.ts
│       │   │   └── team.ts
│       │   ├── db/
│       │   │   ├── schema.ts   # Drizzle schema
│       │   │   ├── index.ts    # DB init
│       │   │   └── migrations/
│       │   ├── middleware/
│       │   │   ├── auth.ts
│       │   │   └── errorHandler.ts
│       │   └── types/
│       │       └── index.ts
│       ├── package.json
│       └── tsconfig.json
├── docs/
│   ├── SPEC.md                 # Full technical spec (generated by spec agent)
│   └── DATABASE.md             # Schema reference
├── package.json                # Monorepo root
└── BRIEF.md                    # This file
```

## Quality Bar
- **Zero unhandled errors** — all API errors caught, user-facing error messages
- **Type safety:** TypeScript strict mode, no `any` types
- **Test coverage:** >70% for critical paths (auth, client CRUD, project allocation)
- **Responsive:** Mobile-first, tested at 375px, 768px, 1440px
- **Accessibility:** WCAG 2.1 AA (form labels, color contrast, keyboard nav)
- **Performance:** Page load <2s, API responses <500ms (p95)
- **Security:** Passwords hashed (bcrypt), JWT in httpOnly cookies, CORS configured, SQL injection prevention (Drizzle ORM)
- **Deployment:** CI/CD pipeline (tests, build, deploy to Render or VPS)

## Done Criteria
1. ✅ GitHub repo created at `sajanforwardai/CRM` with initial commit
2. ✅ Database schema (PostgreSQL, Drizzle migrations)
3. ✅ Authentication (login, JWT, role-based access)
4. ✅ Client management (CRUD, list, detail)
5. ✅ Project management (CRUD, status, team allocation, hours tracking)
6. ✅ Proposal workflow (create, send, mark won/lost)
7. ✅ Dashboard with KPIs and activity feed
8. ✅ Team & capacity management
9. ✅ Tests for critical flows (auth, project creation, team allocation)
10. ✅ Deployed to staging or production
11. ✅ Indexed into intelligence engine
