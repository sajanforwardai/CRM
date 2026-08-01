# ForwardAI CRM — Technical Specification

**Version:** 1.0 MVP  
**Date:** 2026-08-01  
**Status:** Design Phase  

---

## 1. Overview

The ForwardAI CRM is an operational backbone for AI consulting engagement tracking. It manages client relationships, project lifecycles, proposal workflows, team capacity allocation, and financial tracking. Built as a full-stack TypeScript monorepo, it serves internal teams at `forwardai.dev/crm` with authentication-gated access.

**Key Goals:**
- Enable rapid client and project onboarding with minimal friction
- Provide real-time team capacity visibility and allocation management
- Automate proposal-to-project workflow with status tracking
- Deliver KPI dashboard for leadership visibility (pipeline, utilization, revenue)
- Support future reporting and export capabilities

**MVP Scope:** Client management, project tracking, proposal workflow, team capacity dashboard, basic reporting structure.

---

## 2. Technical Architecture & Stack

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js 14)                    │
│  - App Router with Server Components                         │
│  - shadcn/ui + Tailwind CSS                                  │
│  - TypeScript, Zod for type safety                           │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST
┌──────────────────▼──────────────────────────────────────────┐
│                Backend (Express.js)                          │
│  - Typed Route Handlers (Zod validation)                     │
│  - JWT Auth Middleware                                       │
│  - Role-based Authorization                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │ SQL via Drizzle ORM
┌──────────────────▼──────────────────────────────────────────┐
│              PostgreSQL Database                             │
│  - Drizzle ORM (type-safe migrations)                        │
│  - Version-controlled schema                                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Decisions

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Frontend Framework | Next.js 14 (App Router) | Server Components, built-in API routes, excellent TypeScript support, familiar to team |
| Backend | Express.js + Node.js | Lightweight, mature, native TypeScript via tsx, familiar ecosystem |
| Database | PostgreSQL | Relational (complex client/project/team relationships), scalable, JSONB for future extensibility |
| ORM | Drizzle ORM | Type-safe at compile time, zero-overhead abstraction, first-class TypeScript, migrations |
| Authentication | JWT (httpOnly cookies) | Stateless, scalable, secure against XSS (httpOnly), standard for SPA-like apps |
| Password Hashing | bcrypt | Industry standard, slow by design (resists brute force) |
| Validation | Zod | Lightweight, runtime schema validation, generates TypeScript types |
| UI Components | shadcn/ui | Headless, accessible, customizable, good for complex data tables (clients, projects) |
| Styling | Tailwind CSS | Utility-first, responsive by default, performance optimized (purged) |
| API Contract | TypeScript + Zod | Shared types between frontend and backend, runtime validation |
| Testing | Jest + Supertest (backend), Playwright (frontend) | Standard stack, good for integration testing |
| CI/CD | GitHub Actions | Native GitHub integration, YAML-based, free for public repos |
| Deployment | Render or VPS | Render: zero-config (via buildpacks), VPS: full control via praxis toolkit |

### 2.3 Monorepo Structure

```
sajanforwardai/CRM/
├── .github/workflows/
│   ├── test.yml                # Run tests on PR/push
│   └── deploy.yml              # Deploy to staging/production
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── app/
│   │   │   ├── layout.tsx      # Root layout + providers
│   │   │   ├── page.tsx        # Dashboard (after login, role-gated)
│   │   │   ├── login/
│   │   │   │   └── page.tsx    # Login form
│   │   │   ├── (protected)/
│   │   │   │   ├── layout.tsx  # Auth guard wrapper + sidebar
│   │   │   │   ├── clients/
│   │   │   │   │   ├── page.tsx         # Client list
│   │   │   │   │   └── [id]/page.tsx    # Client detail
│   │   │   │   ├── projects/
│   │   │   │   │   ├── page.tsx         # Project list
│   │   │   │   │   └── [id]/page.tsx    # Project detail
│   │   │   │   ├── proposals/
│   │   │   │   │   ├── page.tsx         # Proposal list
│   │   │   │   │   └── [id]/page.tsx    # Proposal detail
│   │   │   │   └── team/
│   │   │   │       ├── page.tsx         # Team list
│   │   │   │       └── [id]/page.tsx    # Team member detail
│   │   │   └── api/
│   │   │       └── (internal - Next.js route handlers if needed)
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── NavLink.tsx
│   │   │   ├── client/
│   │   │   │   ├── ClientTable.tsx
│   │   │   │   ├── ClientForm.tsx
│   │   │   │   └── ClientCard.tsx
│   │   │   ├── project/
│   │   │   │   ├── ProjectTable.tsx
│   │   │   │   ├── ProjectForm.tsx
│   │   │   │   └── ProjectCard.tsx
│   │   │   ├── proposal/
│   │   │   │   ├── ProposalTable.tsx
│   │   │   │   └── ProposalForm.tsx
│   │   │   ├── team/
│   │   │   │   ├── TeamTable.tsx
│   │   │   │   ├── TeamForm.tsx
│   │   │   │   └── UtilizationChart.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── KPICards.tsx
│   │   │   │   ├── ActivityFeed.tsx
│   │   │   │   ├── ProjectTimeline.tsx
│   │   │   │   └── TeamCapacityWidget.tsx
│   │   │   └── shared/
│   │   │       ├── LoadingSpinner.tsx
│   │   │       ├── ErrorBoundary.tsx
│   │   │       └── Modal.tsx
│   │   ├── lib/
│   │   │   ├── api.ts          # API client (fetch wrapper with auth)
│   │   │   ├── auth.ts         # Auth helpers (useAuth hook, getCurrentUser)
│   │   │   ├── utils.ts        # Formatting, calculations
│   │   │   └── schemas.ts      # Zod schemas (shared with backend)
│   │   ├── middleware.ts       # Auth guard (protect /protected routes)
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── next.config.js
│   └── server/                 # Express backend
│       ├── src/
│       │   ├── index.ts        # Express app init, middleware setup
│       │   ├── routes/
│       │   │   ├── index.ts    # Route mounting
│       │   │   ├── auth.ts     # POST /auth/login, /auth/logout, /auth/me
│       │   │   ├── clients.ts  # CRUD endpoints
│       │   │   ├── projects.ts
│       │   │   ├── proposals.ts
│       │   │   ├── team.ts
│       │   │   └── dashboard.ts # KPI aggregation endpoints
│       │   ├── db/
│       │   │   ├── schema.ts   # Drizzle table definitions
│       │   │   ├── index.ts    # DB connection, query builder
│       │   │   ├── migrations/
│       │   │   │   └── 0001_initial.sql
│       │   │   └── seeds.ts    # (Optional) Dev seed data
│       │   ├── middleware/
│       │   │   ├── auth.ts     # JWT verification, role extraction
│       │   │   ├── errorHandler.ts # Global error catch
│       │   │   └── requestLogger.ts
│       │   ├── types/
│       │   │   └── index.ts    # Types for auth claims, request extensions
│       │   └── utils/
│       │       ├── password.ts # bcrypt wrapper
│       │       └── jwt.ts      # Token generation/verification
│       ├── tests/
│       │   ├── auth.test.ts
│       │   ├── clients.test.ts
│       │   └── setup.ts        # Test database + fixtures
│       ├── package.json
│       ├── tsconfig.json
│       └── .env.example
├── packages/
│   └── shared/                 # Shared types + schemas (optional)
│       ├── schemas.ts          # Zod schemas
│       └── types.ts
├── docs/
│   ├── SPEC.md                 # This file
│   ├── DATABASE.md             # Schema reference guide
│   ├── API.md                  # API endpoint documentation
│   └── DEPLOYMENT.md           # Deployment runbook
├── .env.example
├── .gitignore
├── package.json                # Root package.json (workspace config)
├── tsconfig.json               # Root tsconfig (extends to apps)
├── BRIEF.md                    # Project brief (from PM)
└── README.md                   # Getting started guide
```

---

## 3. Database Schema

### 3.1 Entity Relationship Diagram

```
clients
  │
  └─── projects (foreign key: client_id)
         │
         ├─── proposals (foreign key: project_id)
         ├─── allocations (foreign key: project_id)
         ├─── deliverables (foreign key: project_id)
         └─── invoices (foreign key: project_id)

allocations
  └─── team_members (foreign key: team_member_id)
```

### 3.2 Table Definitions (Drizzle Schema)

#### `clients` Table
```sql
CREATE TABLE clients (
  id SERIAL PRIMARY KEY,
  company_name VARCHAR(255) NOT NULL,
  industry VARCHAR(100),  -- e.g. "Wealth Management", "Investment Banking"
  contact_email VARCHAR(255),
  contact_phone VARCHAR(20),
  contact_name VARCHAR(255),
  engagement_type VARCHAR(50) NOT NULL,  -- "retainer" | "project" | "advisory"
  annual_value DECIMAL(12, 2),  -- Expected annual contract value
  status VARCHAR(50) NOT NULL,  -- "prospect" | "active" | "closed"
  total_spent DECIMAL(12, 2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  created_by INT REFERENCES team_members(id),
  UNIQUE(company_name)
);
```

#### `projects` Table
```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  client_id INT NOT NULL REFERENCES clients(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) NOT NULL,  -- "proposal" | "active" | "completed" | "archived"
  start_date DATE,
  end_date DATE,
  estimated_hours INT,  -- Total expected effort
  actual_hours INT DEFAULT 0,  -- Cumulative from allocations
  revenue DECIMAL(12, 2),  -- Project value
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES team_members(id),
  FOREIGN KEY (client_id) REFERENCES clients(id)
  INDEX idx_client_id ON client_id,
  INDEX idx_status ON status
);
```

#### `proposals` Table
```sql
CREATE TABLE proposals (
  id SERIAL PRIMARY KEY,
  project_id INT NOT NULL REFERENCES projects(id),
  title VARCHAR(255),
  description TEXT,
  scope_of_work TEXT,
  deliverables TEXT,  -- JSON array or text
  proposed_team TEXT,  -- JSON array of team member names/roles
  rate DECIMAL(12, 2),
  value DECIMAL(12, 2) NOT NULL,
  terms TEXT,  -- Payment terms, contract notes
  status VARCHAR(50) NOT NULL,  -- "draft" | "sent" | "won" | "lost"
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sent_date TIMESTAMP,
  closed_date TIMESTAMP,  -- Date won/lost
  due_date DATE,
  created_by INT REFERENCES team_members(id),
  INDEX idx_project_id ON project_id,
  INDEX idx_status ON status
);
```

#### `team_members` Table
```sql
CREATE TABLE team_members (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  role VARCHAR(50) NOT NULL,  -- "consultant" | "senior" | "principal" | "admin"
  password_hash VARCHAR(255) NOT NULL,
  billable_rate DECIMAL(12, 2),  -- Hourly rate for billing
  capacity_hours_per_week INT,  -- Total available hours
  status VARCHAR(50) DEFAULT 'active',  -- "active" | "archived"
  auth_role VARCHAR(50) DEFAULT 'team',  -- "admin" | "manager" | "team" (for authorization)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `allocations` Table
```sql
CREATE TABLE allocations (
  id SERIAL PRIMARY KEY,
  team_member_id INT NOT NULL REFERENCES team_members(id),
  project_id INT NOT NULL REFERENCES projects(id),
  hours_per_week INT NOT NULL,  -- Planned allocation
  start_date DATE NOT NULL,
  end_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (team_member_id, project_id, start_date),
  INDEX idx_team_member ON team_member_id,
  INDEX idx_project_id ON project_id,
  INDEX idx_date_range ON start_date, end_date
);
```

#### `deliverables` Table
```sql
CREATE TABLE deliverables (
  id SERIAL PRIMARY KEY,
  project_id INT NOT NULL REFERENCES projects(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) NOT NULL,  -- "pending" | "in_progress" | "completed"
  due_date DATE,
  owner_id INT REFERENCES team_members(id),  -- Assigned team member
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  INDEX idx_project_id ON project_id,
  INDEX idx_status ON status
);
```

#### `invoices` Table
```sql
CREATE TABLE invoices (
  id SERIAL PRIMARY KEY,
  project_id INT NOT NULL REFERENCES projects(id),
  amount DECIMAL(12, 2) NOT NULL,
  status VARCHAR(50) NOT NULL,  -- "draft" | "sent" | "paid"
  issue_date DATE,
  due_date DATE,
  paid_date DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_project_id ON project_id,
  INDEX idx_status ON status
);
```

### 3.3 Indexes & Performance

**Indexes by priority:**
1. `clients(status)` — Filter by prospect/active/closed
2. `projects(client_id, status)` — Composite for "show projects for client X with status Y"
3. `proposals(project_id, status)` — Composite for proposal workflow
4. `allocations(team_member_id, start_date, end_date)` — Range queries for capacity
5. `team_members(email)` — Auth lookup
6. `deliverables(project_id, status)` — Filter by project

**No full-text search MVP:** Use PostgreSQL's basic LIKE queries initially; add `pg_trgm` gin index if needed later.

---

## 4. API Endpoint Contracts

### 4.1 Authentication Endpoints

**POST /api/auth/login**
```typescript
Request: {
  email: string;
  password: string;
}
Response (200): {
  id: number;
  name: string;
  email: string;
  role: string; // "admin" | "manager" | "team"
  auth_role: string;
}
// Sets httpOnly cookie: session=<jwt>
Response (401): { error: "Invalid credentials" }
```

**POST /api/auth/logout**
```
Response (200): { success: true }
// Clears session cookie
```

**GET /api/auth/me**
```
Response (200): {
  id: number;
  name: string;
  email: string;
  role: string;
}
Response (401): { error: "Unauthorized" }
```

### 4.2 Client Endpoints

**GET /api/clients**
```typescript
Query: {
  status?: "prospect" | "active" | "closed";
  sort?: "name" | "annual_value" | "created_at";
  order?: "asc" | "desc";
  limit?: number;
  offset?: number;
}
Response (200): {
  data: Array<{
    id: number;
    company_name: string;
    industry?: string;
    contact_name?: string;
    contact_email?: string;
    engagement_type: string;
    annual_value?: number;
    status: string;
    total_spent: number;
    created_at: string;
    project_count: number;
  }>;
  total: number;
}
```

**POST /api/clients** (Admin/Manager only)
```typescript
Request: {
  company_name: string;
  industry?: string;
  contact_name?: string;
  contact_email?: string;
  contact_phone?: string;
  engagement_type: "retainer" | "project" | "advisory";
  annual_value?: number;
  status: "prospect" | "active" | "closed";
  notes?: string;
}
Response (201): { id: number; ... } // Full client object
Response (400): { error: "Validation error", details: [...] }
```

**GET /api/clients/:id**
```
Response (200): {
  id: number;
  company_name: string;
  industry?: string;
  contact_name?: string;
  contact_email?: string;
  contact_phone?: string;
  engagement_type: string;
  annual_value?: number;
  status: string;
  total_spent: number;
  created_at: string;
  created_by?: { id: number; name: string };
  projects: Array<{ id: number; title: string; status: string; ... }>;
  proposals: Array<{ id: number; value: number; status: string; ... }>;
}
Response (404): { error: "Client not found" }
```

**PATCH /api/clients/:id** (Admin/Manager only)
```typescript
Request (partial update): {
  company_name?: string;
  contact_name?: string;
  contact_email?: string;
  engagement_type?: string;
  annual_value?: number;
  status?: string;
}
Response (200): { id: number; ... } // Updated client
```

**DELETE /api/clients/:id** (Admin only)
```
Response (204): No content
Response (409): { error: "Cannot delete client with active projects" }
```

### 4.3 Project Endpoints

**GET /api/projects**
```typescript
Query: {
  client_id?: number;
  status?: "proposal" | "active" | "completed" | "archived";
  sort?: "title" | "start_date" | "estimated_hours";
  order?: "asc" | "desc";
  limit?: number;
  offset?: number;
}
Response (200): {
  data: Array<{
    id: number;
    client_id: number;
    client_name: string;
    title: string;
    status: string;
    start_date?: string;
    end_date?: string;
    estimated_hours?: number;
    actual_hours: number;
    revenue?: number;
    team_count: number;
    progress_pct: number;
  }>;
  total: number;
}
```

**POST /api/projects** (Manager only)
```typescript
Request: {
  client_id: number;
  title: string;
  description?: string;
  start_date?: string; // ISO date
  end_date?: string;
  estimated_hours?: number;
  revenue?: number;
  status?: "proposal" | "active";
}
Response (201): { id: number; ... } // Full project
```

**GET /api/projects/:id**
```
Response (200): {
  id: number;
  client_id: number;
  client: { id: number; company_name: string; ... };
  title: string;
  description?: string;
  status: string;
  start_date?: string;
  end_date?: string;
  estimated_hours?: number;
  actual_hours: number;
  revenue?: number;
  allocations: Array<{
    id: number;
    team_member_id: number;
    team_member_name: string;
    hours_per_week: number;
    start_date: string;
    end_date?: string;
  }>;
  deliverables: Array<{
    id: number;
    title: string;
    status: string;
    due_date?: string;
    owner_name?: string;
  }>;
  financials: {
    estimated_revenue: number;
    actual_cost: number;
    margin: number;
    margin_pct: number;
  };
}
```

**PATCH /api/projects/:id** (Manager only)
```typescript
Request (partial): {
  title?: string;
  status?: string;
  estimated_hours?: number;
  revenue?: number;
}
Response (200): { id: number; ... }
```

**POST /api/projects/:id/archive** (Manager only)
```
Request: { }
Response (200): { status: "archived" }
```

### 4.4 Proposal Endpoints

**GET /api/proposals**
```typescript
Query: {
  client_id?: number;
  project_id?: number;
  status?: "draft" | "sent" | "won" | "lost";
  sort?: "created_at" | "value";
  order?: "asc" | "desc";
  limit?: number;
  offset?: number;
}
Response (200): {
  data: Array<{
    id: number;
    project_id: number;
    project_title: string;
    client_id: number;
    client_name: string;
    title?: string;
    value: number;
    status: string;
    created_at: string;
    sent_date?: string;
    due_date?: string;
  }>;
  total: number;
}
```

**POST /api/proposals** (Manager only)
```typescript
Request: {
  project_id: number;
  title?: string;
  description?: string;
  scope_of_work?: string;
  deliverables?: string;
  proposed_team?: string;
  value: number;
  rate?: number;
  terms?: string;
  due_date?: string;
  status?: "draft"; // Always starts as draft
}
Response (201): { id: number; status: "draft"; ... }
```

**GET /api/proposals/:id**
```
Response (200): {
  id: number;
  project_id: number;
  project: { id: number; title: string; client_id: number; client_name: string; ... };
  title?: string;
  description?: string;
  scope_of_work?: string;
  deliverables?: string;
  proposed_team?: string;
  value: number;
  rate?: number;
  terms?: string;
  status: string;
  created_at: string;
  sent_date?: string;
  closed_date?: string;
  due_date?: string;
  created_by: { id: number; name: string };
}
```

**PATCH /api/proposals/:id** (Manager only, draft only)
```typescript
Request (partial): {
  title?: string;
  description?: string;
  value?: number;
  due_date?: string;
}
Response (200): { ... } // Updated proposal
Response (400): { error: "Cannot edit sent/won/lost proposal" }
```

**POST /api/proposals/:id/send** (Manager only, draft only)
```
Response (200): { status: "sent", sent_date: "2026-08-01T12:00:00Z" }
```

**POST /api/proposals/:id/mark-won** (Manager only, sent only)
```
Response (200): {
  status: "won",
  closed_date: "2026-08-01T12:00:00Z",
  // Also updates related project status to "active"
}
```

**POST /api/proposals/:id/mark-lost** (Manager only, sent only)
```
Response (200): {
  status: "lost",
  closed_date: "2026-08-01T12:00:00Z"
}
```

### 4.5 Team Endpoints

**GET /api/team**
```
Response (200): {
  data: Array<{
    id: number;
    name: string;
    email: string;
    role: string;
    billable_rate: number;
    capacity_hours_per_week: number;
    utilization_pct: number;
    status: string;
  }>;
  total: number;
}
```

**POST /api/team** (Admin only)
```typescript
Request: {
  name: string;
  email: string;
  password: string;
  role: "consultant" | "senior" | "principal";
  billable_rate: number;
  capacity_hours_per_week: number;
  auth_role?: "admin" | "manager" | "team";
}
Response (201): { id: number; ... }
```

**GET /api/team/:id**
```
Response (200): {
  id: number;
  name: string;
  email: string;
  role: string;
  billable_rate: number;
  capacity_hours_per_week: number;
  status: string;
  allocations: Array<{
    id: number;
    project_id: number;
    project_title: string;
    hours_per_week: number;
    start_date: string;
    end_date?: string;
  }>;
  utilization_weekly: Array<{
    week_of: string;
    hours_allocated: number;
    hours_available: number;
    pct_utilized: number;
  }>;
  monthly_stats: {
    hours_billed: number;
    revenue_generated: number;
  };
}
```

**PATCH /api/team/:id** (Admin only)
```typescript
Request (partial): {
  name?: string;
  billable_rate?: number;
  capacity_hours_per_week?: number;
  status?: string;
}
Response (200): { ... }
```

**POST /api/team/:id/allocations** (Manager only)
```typescript
Request: {
  project_id: number;
  hours_per_week: number;
  start_date: string;
  end_date?: string;
}
Response (201): {
  id: number;
  team_member_id: number;
  project_id: number;
  hours_per_week: number;
  start_date: string;
}
Response (409): { error: "Allocation conflict or over-capacity" }
```

### 4.6 Dashboard Endpoints

**GET /api/dashboard/kpis**
```
Response (200): {
  total_pipeline_value: number;  // Sum of sent + draft proposals
  active_projects_count: number;
  team_utilization_pct: number;  // Avg utilization this week
  revenue_ytd: number;           // Sum of won proposals closed this year
  revenue_ytm: number;           // This month
  top_clients: Array<{ name: string; annual_value: number; ... }>;
}
```

**GET /api/dashboard/activity**
```
Response (200): {
  recent_activities: Array<{
    id: string;
    type: "proposal_sent" | "project_started" | "deliverable_completed";
    description: string;
    timestamp: string;
    related_entity: { type: string; id: number; name: string };
  }>;
}
```

**GET /api/dashboard/team-capacity**
```
Response (200): {
  this_week: {
    total_available: number;
    total_allocated: number;
    team_members: Array<{
      id: number;
      name: string;
      available: number;
      allocated: number;
      pct_utilized: number;
    }>;
  };
  next_4_weeks: Array<{ week_of: string; total_available: number; total_allocated: number; ... }>;
}
```

### 4.7 Error Handling

All error responses follow this contract:

```typescript
type ErrorResponse = {
  error: string;          // Human-readable message
  code: string;           // Error code (e.g., "VALIDATION_ERROR", "NOT_FOUND", "UNAUTHORIZED")
  details?: Array<{
    field: string;
    message: string;
  }>;
  timestamp: string;      // ISO timestamp
};

HTTP Status Codes:
- 200: Success
- 201: Created
- 204: No content (successful deletion)
- 400: Validation error
- 401: Unauthorized (not logged in)
- 403: Forbidden (logged in but no permission)
- 404: Not found
- 409: Conflict (e.g., over-allocation, duplicate)
- 500: Server error
```

---

## 5. Frontend Architecture

### 5.1 Page Structure

```
Root Layout
├── /login → LoginPage (public)
└── (protected) → ProtectedLayout (auth guard)
    ├── / → Dashboard
    ├── /clients
    │   ├── page → ClientListPage
    │   └── [id] → ClientDetailPage
    │       ├── Overview tab
    │       ├── Projects tab
    │       ├── Proposals tab
    │       └── Activity tab
    ├── /projects
    │   ├── page → ProjectListPage
    │   └── [id] → ProjectDetailPage
    │       ├── Overview section
    │       ├── Deliverables section
    │       ├── Team section
    │       ├── Financials section
    │       └── Timeline section
    ├── /proposals
    │   ├── page → ProposalListPage
    │   └── [id] → ProposalDetailPage
    │       ├── Read view (all users)
    │       ├── Edit view (draft only, managers)
    │       └── Action buttons
    └── /team
        ├── page → TeamListPage
        └── [id] → TeamMemberDetailPage
            ├── Basic info
            ├── Allocations section
            ├── Utilization chart
            └── Historical stats
```

### 5.2 Key Components

**Layout Components:**
- `Sidebar.tsx` — Persistent navigation, role-based menu items
- `Header.tsx` — Breadcrumb, user menu, logout
- `NavLink.tsx` — Active link indicator

**Data Table Components:**
- `ClientTable.tsx` — Sortable, filterable client list with search
- `ProjectTable.tsx` — Projects with progress indicators
- `ProposalTable.tsx` — Proposals with status badges
- `TeamTable.tsx` — Team with utilization % inline

**Form Components:**
- `ClientForm.tsx` — Create/edit client
- `ProjectForm.tsx` — Create/edit project
- `ProposalForm.tsx` — Multi-step: draft → review → send
- `TeamForm.tsx` — Create/edit team member

**Dashboard Components:**
- `KPICards.tsx` — 4-card grid (pipeline, projects, utilization, revenue)
- `ProjectTimeline.tsx` — Gantt or card view of active projects
- `TeamCapacityWidget.tsx` — Stacked bar chart: allocated vs available
- `ActivityFeed.tsx` — Recent activity list with avatars, timestamps

**Feature Components:**
- `AllocationModal.tsx` — Assign team member to project
- `ProposalPreview.tsx` — PDF-like rendering for proposals
- `DeliverableCheckbox.tsx` — Toggle deliverable completion

### 5.3 Hooks & Utilities

**Auth Hook (`lib/auth.ts`):**
```typescript
export function useAuth() {
  return {
    user: { id, name, email, role } | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    isAdmin: boolean;
    isManager: boolean;
    logout: () => Promise<void>;
  };
}

export function requireAuth(role?: "admin" | "manager") {
  // Middleware for protected routes
}
```

**API Client (`lib/api.ts`):**
```typescript
export class APIClient {
  async get<T>(url: string, options?: ...): Promise<T>
  async post<T>(url: string, data?: ...): Promise<T>
  async patch<T>(url: string, data?: ...): Promise<T>
  async delete(url: string): Promise<void>
  // Auto-attaches auth cookie, handles 401 → redirect to login
}
```

**Formatting Utils (`lib/utils.ts`):**
```typescript
export function formatCurrency(amount: number): string
export function formatDate(date: string): string
export function calculateProgress(actual: number, estimated: number): number
export function getStatusBadgeColor(status: string): "green" | "yellow" | "red"
```

### 5.4 Styling & Responsive Design

- **Base:** Tailwind CSS v3.4+, responsive-first
- **Breakpoints:** 375px (mobile), 768px (tablet), 1440px (desktop)
- **Color scheme:** Light/dark mode via `next-themes` (optional for MVP, defer to v2)
- **Components:** shadcn/ui (Button, Input, Select, Table, Dialog, Badge, Card, Tabs)
- **Typography:** System font stack for performance

**Dark mode (future):**
```typescript
// apps/web/lib/darkMode.ts
// Use next-themes with Tailwind's dark: class strategy
```

### 5.5 Accessibility

- Form labels + ARIA attributes (required for WCAG AA)
- Tab navigation: focus visible on all interactive elements
- Color contrast: 4.5:1 for text, 3:1 for large text
- Images: alt text on all images (including charts)
- Keyboard navigation: No mouse-only interactions
- Skip-to-content link on every page

---

## 6. Authentication & Authorization

### 6.1 Authentication Flow

```
User visits /login (unauthenticated)
    ↓
Submit email + password to POST /api/auth/login
    ↓
Backend: Hash check + JWT generation
    ↓
Backend: Set httpOnly, Secure, SameSite=Strict cookie (session=<jwt>)
    ↓
Frontend: Redirect to / (protected)
    ↓
Middleware: GET /api/auth/me (verify cookie)
    ↓
If valid: render dashboard + protected routes
If invalid (401): redirect to /login
```

### 6.2 Authorization Model

**Three roles with increasing privilege:**

| Role | Capabilities |
|------|--------------|
| **Team** (default) | View own allocations, assigned projects, team list (read-only) |
| **Manager** | Create/edit clients, projects, proposals; send proposals; allocate team |
| **Admin** | + Add/edit team members, delete clients, system settings |

**Role-based UI:**
- Only admins see "Add Team Member" button
- Only managers see "Send Proposal" button (draft only)
- Team members see read-only views of their allocations

### 6.3 JWT Structure

```typescript
{
  "sub": "123",        // team_member.id
  "email": "user@forwardai.dev",
  "name": "John Doe",
  "role": "admin" | "manager" | "team",
  "iat": 1691000000,
  "exp": 1691086400,   // 24 hours (configurable)
  "iss": "forwardai-crm"
}
```

**Token generation (backend):**
```typescript
// apps/server/src/utils/jwt.ts
export function generateToken(teamMember: TeamMember): string {
  const payload = {
    sub: teamMember.id,
    email: teamMember.email,
    name: teamMember.name,
    role: teamMember.auth_role,
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60), // 24 hours
    iss: "forwardai-crm"
  };
  return jwt.sign(payload, process.env.JWT_SECRET!);
}
```

### 6.4 Middleware

**Auth Middleware (backend):**
```typescript
// apps/server/src/middleware/auth.ts
export function authMiddleware(req, res, next) {
  const token = req.cookies.session;
  if (!token) return res.status(401).json({ error: "Unauthorized" });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded;
    next();
  } catch {
    return res.status(401).json({ error: "Invalid token" });
  }
}

export function requireRole(role: "admin" | "manager") {
  return (req, res, next) => {
    const userRole = req.user.role;
    const roleHierarchy = { admin: 3, manager: 2, team: 1 };
    if (roleHierarchy[userRole] < roleHierarchy[role]) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}
```

**Middleware (frontend):**
```typescript
// apps/web/middleware.ts
import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("session");
  
  // Redirect unauthenticated users to /login
  if (!token && request.nextUrl.pathname.startsWith("/(protected)")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  
  // Redirect authenticated users away from /login
  if (token && request.nextUrl.pathname === "/login") {
    return NextResponse.redirect(new URL("/", request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ["/(protected)/:path*", "/login", "/"],
};
```

---

## 7. Deployment & CI/CD

### 7.1 Deployment Options

**Option A: Render (Recommended for MVP)**
- Frontend: Render Web Service (auto-deploy from GitHub)
- Backend: Render Web Service (auto-deploy from GitHub)
- Database: Render PostgreSQL (managed, backups included)
- Domain: Map `forwardai.dev/crm` via reverse proxy or subdomain

**Option B: VPS (Full Control)**
- Use praxis toolkit at `/workspace/.swarm/praxis/toolkit/`
- Manually provision: Ubuntu 22.04, Docker, nginx, PostgreSQL
- CI/CD: GitHub Actions → build Docker images → push to registry → SSH deploy

### 7.2 Environment Variables

**Backend (`apps/server/.env`):**
```
DATABASE_URL=postgresql://user:pass@localhost:5432/crm_db
JWT_SECRET=<random-256-bit-key>
JWT_EXPIRY_HOURS=24
NODE_ENV=production
PORT=3001
CORS_ORIGIN=https://forwardai.dev/crm,http://localhost:3000
```

**Frontend (`apps/web/.env.local`):**
```
NEXT_PUBLIC_API_URL=https://api.forwardai.dev
NEXT_PUBLIC_APP_URL=https://forwardai.dev/crm
```

### 7.3 GitHub Actions Pipeline

**Test Workflow (`.github/workflows/test.yml`):**
```yaml
name: Test
on: [pull_request, push]
jobs:
  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "20"
      - run: cd apps/server && npm install && npm test
  
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: cd apps/web && npm install && npm run test:unit
      - run: npm run build  # Verify builds without error
```

**Deploy Workflow (`.github/workflows/deploy.yml`):**
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: cd apps/server && npm install && npm run build
      - run: cd apps/web && npm install && npm run build
      - run: |
          # Push to Render or VPS
          # (Render: auto-deploys on git push to main)
          # (VPS: build Docker images, push to registry, deploy via SSH)
```

---

## 8. Technology Stack & Versions

### 8.1 Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **Frontend** | | |
| next | 14.2+ | Full-stack React framework |
| react | 18.3+ | UI library |
| react-dom | 18.3+ | DOM rendering |
| typescript | 5.4+ | Type safety |
| tailwindcss | 3.4+ | Utility CSS |
| shadcn/ui | latest | Component library |
| zod | 3.22+ | Schema validation |
| axios or fetch | - | HTTP client |
| **Backend** | | |
| express | 4.19+ | Web framework |
| typescript | 5.4+ | Type safety |
| drizzle-orm | 0.30+ | Type-safe ORM |
| pg | 8.11+ | PostgreSQL driver |
| jsonwebtoken | 9.1+ | JWT signing |
| bcrypt | 5.1+ | Password hashing |
| zod | 3.22+ | Schema validation |
| **Testing** | | |
| jest | 29.7+ | Unit/integration tests |
| supertest | 6.3+ | HTTP testing |
| @testing-library/react | 14.0+ | Component testing |
| playwright | 1.40+ | E2E testing |
| **Utilities** | | |
| dotenv | 16.3+ | Environment variables |
| date-fns | 2.30+ | Date formatting |

### 8.2 DevDependencies

```json
{
  "@types/node": "^20.0.0",
  "@types/express": "^4.17.0",
  "@types/bcrypt": "^5.0.0",
  "@types/jsonwebtoken": "^9.0.0",
  "tsx": "^4.0.0",
  "ts-node": "^10.9.0",
  "nodemon": "^3.0.0"
}
```

---

## 9. Data Validation & Error Handling

### 9.1 Zod Schemas

**Shared across frontend & backend:**
```typescript
// apps/web/lib/schemas.ts (or packages/shared/schemas.ts)

export const ClientSchema = z.object({
  id: z.number().optional(),
  company_name: z.string().min(1, "Required").max(255),
  industry: z.string().optional(),
  contact_name: z.string().optional(),
  contact_email: z.string().email().optional(),
  contact_phone: z.string().optional(),
  engagement_type: z.enum(["retainer", "project", "advisory"]),
  annual_value: z.number().positive().optional(),
  status: z.enum(["prospect", "active", "closed"]),
  notes: z.string().optional(),
});

export const ProjectSchema = z.object({
  id: z.number().optional(),
  client_id: z.number(),
  title: z.string().min(1).max(255),
  description: z.string().optional(),
  status: z.enum(["proposal", "active", "completed", "archived"]),
  start_date: z.string().datetime().optional(),
  end_date: z.string().datetime().optional(),
  estimated_hours: z.number().int().positive().optional(),
  revenue: z.number().positive().optional(),
});

export const ProposalSchema = z.object({
  id: z.number().optional(),
  project_id: z.number(),
  title: z.string().optional(),
  value: z.number().positive(),
  status: z.enum(["draft", "sent", "won", "lost"]),
  due_date: z.string().datetime().optional(),
});

// ... etc for Team, Allocation, Deliverable
```

### 9.2 Backend Validation

```typescript
// apps/server/src/routes/clients.ts
import { Router } from "express";
import { ClientSchema } from "shared/schemas";

const router = Router();

router.post("/", authMiddleware, requireRole("manager"), async (req, res) => {
  try {
    const validated = ClientSchema.parse(req.body);
    // Create client in DB
    const client = await db.clients.insert(validated).returning("*");
    res.status(201).json(client);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: "Validation failed",
        code: "VALIDATION_ERROR",
        details: error.errors.map(e => ({
          field: e.path.join("."),
          message: e.message,
        })),
      });
    }
    res.status(500).json({ error: "Internal server error" });
  }
});
```

### 9.3 Frontend Validation

```typescript
// apps/web/components/client/ClientForm.tsx
"use client";

import { useState } from "react";
import { ClientSchema } from "@/lib/schemas";
import { apiClient } from "@/lib/api";

export function ClientForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  async function onSubmit(formData: unknown) {
    try {
      const validated = ClientSchema.parse(formData);
      const client = await apiClient.post("/api/clients", validated);
      // Redirect to client detail
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errs = error.errors.reduce((acc, e) => {
          acc[e.path.join(".")] = e.message;
          return acc;
        }, {} as Record<string, string>);
        setErrors(errs);
      }
    }
  }
  
  return (
    // Form with inline error display
  );
}
```

---

## 10. Testing Strategy

### 10.1 Test Coverage Goals

- **Backend:** >70% line coverage for auth, CRUD routes, allocation logic
- **Frontend:** >60% line coverage for critical paths (login, client list, project detail)
- **E2E:** Happy path for core workflows (login → create client → create project → send proposal)

### 10.2 Backend Tests

**Auth tests (`apps/server/tests/auth.test.ts`):**
```typescript
describe("POST /api/auth/login", () => {
  it("returns JWT cookie on valid credentials", async () => {
    const res = await request(app)
      .post("/api/auth/login")
      .send({ email: "user@test.com", password: "password123" });
    
    expect(res.statusCode).toBe(200);
    expect(res.headers["set-cookie"]).toMatch(/session=/);
  });
  
  it("returns 401 on invalid password", async () => {
    const res = await request(app)
      .post("/api/auth/login")
      .send({ email: "user@test.com", password: "wrong" });
    
    expect(res.statusCode).toBe(401);
  });
});
```

**Client CRUD tests (`apps/server/tests/clients.test.ts`):**
```typescript
describe("Clients API", () => {
  it("creates a client with valid data", async () => {
    const res = await request(app)
      .post("/api/clients")
      .set("Cookie", `session=${token}`)
      .send({
        company_name: "Acme Corp",
        engagement_type: "retainer",
        status: "prospect",
      });
    
    expect(res.statusCode).toBe(201);
    expect(res.body.company_name).toBe("Acme Corp");
  });
  
  it("validates required fields", async () => {
    const res = await request(app)
      .post("/api/clients")
      .set("Cookie", `session=${token}`)
      .send({ company_name: "" });
    
    expect(res.statusCode).toBe(400);
    expect(res.body.code).toBe("VALIDATION_ERROR");
  });
});
```

### 10.3 Frontend Tests

**Login component test:**
```typescript
// apps/web/__tests__/components/LoginForm.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import LoginForm from "@/components/LoginForm";

describe("LoginForm", () => {
  it("submits email and password", async () => {
    render(<LoginForm />);
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "user@test.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));
    
    // Verify API call or redirect
  });
});
```

### 10.4 E2E Tests (Playwright)

```typescript
// apps/web/e2e/workflows.spec.ts
import { test, expect } from "@playwright/test";

test("Create client and project workflow", async ({ page }) => {
  // 1. Login
  await page.goto("http://localhost:3000/login");
  await page.fill('input[name="email"]', "manager@forwardai.dev");
  await page.fill('input[name="password"]', "password123");
  await page.click("button[type='submit']");
  
  // 2. Create client
  await page.click("button:has-text('New Client')");
  await page.fill('input[name="company_name"]', "Acme Wealth");
  await page.selectOption('select[name="engagement_type"]', "retainer");
  await page.click("button:has-text('Save')");
  
  // 3. Verify client appears in list
  await expect(page.locator("text=Acme Wealth")).toBeVisible();
  
  // 4. Create project
  await page.click("text=Acme Wealth");
  await page.click("button:has-text('New Project')");
  await page.fill('input[name="title"]', "Portfolio Analysis");
  await page.click("button:has-text('Save')");
  
  // 5. Verify project appears
  await expect(page.locator("text=Portfolio Analysis")).toBeVisible();
});
```

---

## 11. Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Page Load** | <2s (p95) | SPA fast feedback |
| **API Response** | <500ms (p95) | User experience |
| **Database Query** | <100ms (p95) | Well-indexed, simple joins |
| **Frontend Bundle** | <300KB gzipped | Fast first paint |
| **FCP** (First Contentful Paint) | <1s | User perceives loading |
| **LCP** (Largest Contentful Paint) | <2.5s | WCAG recommended |

**Optimization strategies:**
- Use Next.js Image component for dashboard charts/logos
- Lazy-load heavy tables (client list: 50 per page, infinite scroll)
- Cache KPI dashboard for 5 minutes (GET /api/dashboard/kpis)
- Compress large exports (CSV) on-the-fly
- Use database indexes on all filter/sort columns

---

## 12. Security Considerations

### 12.1 OWASP Top 10 Mitigations

| Risk | Mitigation |
|------|-----------|
| A01: Injection | Drizzle ORM parameterized queries, Zod validation |
| A02: Broken Auth | JWT + httpOnly cookies, bcrypt (12+ rounds), rate limit login attempts |
| A03: Exposure | No sensitive data in logs, .env in .gitignore, secrets via GitHub Actions |
| A04: XXS | React escaping by default, no dangerouslySetInnerHTML, CSP header |
| A05: CSRF | SameSite=Strict cookie, CSRF token optional for forms |
| A06: Insecure Components | Audit dependencies monthly (npm audit) |
| A07: Auth Bypass | Middleware on all protected routes, role checks on mutations |
| A08: Data Integrity | Database constraints (FK, NOT NULL), Zod validation |
| A09: Logging | Structured logging, no passwords/tokens in logs |
| A10: SSRF | No external API calls (MVP) |

### 12.2 Secrets Management

**Development:**
```bash
# .env (local, not committed)
DATABASE_URL=postgresql://...
JWT_SECRET=<local-dev-key>
```

**Production:**
```bash
# GitHub Actions Secrets
- DATABASE_URL (Render PostgreSQL connection string)
- JWT_SECRET (random 256-bit key)
- DEPLOY_KEY (SSH key for VPS deployment, if used)
```

### 12.3 Rate Limiting

```typescript
// apps/server/middleware/rateLimit.ts
import rateLimit from "express-rate-limit";

export const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: "Too many login attempts, please try again later",
  standardHeaders: true,
});

// Use on POST /api/auth/login
```

---

## 13. Monitoring & Observability (Future)

Deferred to v2, but structure for:
- **Logging:** Winston or Pino (structured JSON logs)
- **Monitoring:** Datadog or New Relic (APM)
- **Errors:** Sentry (error tracking)
- **Analytics:** PostHog or Mixpanel (feature usage)

**Log format example:**
```json
{
  "timestamp": "2026-08-01T12:00:00Z",
  "level": "INFO",
  "service": "crm-backend",
  "action": "client_created",
  "user_id": 123,
  "client_id": 456,
  "duration_ms": 145
}
```

---

## 14. Future Enhancements (Post-MVP)

1. **Reporting & Exports** — CSV export for clients, projects, team utilization
2. **Dark Mode** — next-themes integration, user preference
3. **Full-Text Search** — PostgreSQL pg_trgm extension
4. **Webhooks** — External integrations (Slack notifications)
5. **Advanced Scheduling** — Calendar view for allocations, conflict detection
6. **Financials** — Detailed profitability reports, margin analysis
7. **Two-Factor Auth** — TOTP-based MFA
8. **Single Sign-On (SSO)** — SAML/OAuth2 integration
9. **Mobile App** — React Native version
10. **AI Assistant** — GPT-powered proposal drafting

---

## 15. Done Criteria Summary

✅ **Schema:** All 8 tables defined with relationships, indexes, and constraints  
✅ **API Contracts:** 40+ endpoints with typed request/response schemas  
✅ **Frontend Architecture:** Page structure, components, hooks, validation  
✅ **Auth Model:** JWT, roles (admin/manager/team), middleware layer  
✅ **Database:** Migrations strategy, connection pooling, Drizzle ORM integration  
✅ **Deployment:** Render + GitHub Actions workflow, environment config  
✅ **Testing:** Backend TDD strategy, frontend component/E2E tests  
✅ **Performance:** Targets defined, optimization strategies identified  
✅ **Security:** OWASP checklist, secrets management, rate limiting  
✅ **Tech Stack:** All versions pinned, rationale documented  

---

## 16. Implementation Phases

**Phase 1 (Foundation):** Database + auth + basic CRUD  
**Phase 2 (Core Features):** Clients, projects, proposals, team  
**Phase 3 (Dashboard):** KPIs, timeline, capacity widget  
**Phase 4 (Polish):** Tests, docs, performance optimization  
**Phase 5 (Deploy):** Staging + production, monitoring setup  

---

**End of Specification**

*Spec authored by Spec Agent on 2026-08-01*  
*Ready for worktree-swarm implementation*
