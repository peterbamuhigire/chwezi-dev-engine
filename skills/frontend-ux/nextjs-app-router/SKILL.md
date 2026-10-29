---
name: nextjs-app-router
description: Use when implementing or reviewing a Next.js App Router application with server and client components, route handlers, Proxy migration, caching, authentication, streaming, or deployment. Use react-development for framework-neutral components and api-design-first for external APIs.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Next.js App Router Patterns
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Next.js App Router patterns for production — server/client components, parallel routes, Proxy migration, server-side authorization, caching, background jobs (BullMQ), data fetching, authentication, deployment, and CI/CD.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | Route + middleware test plan | Markdown doc covering server/client component boundaries, parallel routes, and middleware | `docs/web/nextjs-route-tests.md` |
| Security | RBAC three-tier configuration note | Markdown doc covering middleware / server action / data-access guards | `docs/web/nextjs-rbac.md` |

## References

- Use the links and companion skills already referenced in this file when deeper context is needed.
- For private tenant-owned data and auth/cache boundaries, load [`references/tenant-data-security.md`](references/tenant-data-security.md).
<!-- dual-compat-end -->
## Project Setup

```bash
npx create-next-app@latest my-app \
  --typescript --tailwind --eslint --app --src-dir
```

### Folder Structure (App Router)

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home route /
├── (marketing)/        # Route group — no URL segment
├── @notifications/     # Parallel route slot
│   └── page.tsx
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx
│   ├── loading.tsx     # Suspense fallback
│   ├── error.tsx       # Error boundary ('use client')
│   └── not-found.tsx
└── api/users/route.ts  # GET/POST /api/users
```

---

## Server vs Client Components

```tsx
// Server component (default) — async, zero JS to client
// Public, non-sensitive example only. For user-specific data, authenticate at
// the data-access boundary and avoid shared/static caching; see the tenant
// data security reference below.
export default async function UsersPage() {
  const users = await fetch('https://api.example.com/users', {
    cache: 'force-cache',        // static
    // next: { revalidate: 60 } // ISR
    // cache: 'no-store'        // SSR
  }).then(r => r.json());
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Client component — needs interactivity, browser APIs
'use client';
export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>;
}
```

**Rule:** Push `'use client'` as far down the tree as possible.

---

## Routing

| File | Route |
|------|-------|
| `app/page.tsx` | `/` |
| `app/blog/[slug]/page.tsx` | `/blog/:slug` |
| `app/shop/[...slug]/page.tsx` | `/shop/*` catch-all |
| `app/(auth)/login/page.tsx` | `/login` (route group) |
| `app/@modal/page.tsx` | Parallel slot |

### Dynamic Routes + generateStaticParams

```tsx
export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await fetchPost(slug);
  return <article><h1>{post.title}</h1></article>;
}
export async function generateStaticParams() {
  const posts = await fetchAllPosts();
  return posts.map(p => ({ slug: p.slug }));
}
```

### Parallel Routes (@slot)

```tsx
// app/support/layout.tsx — load @tickets and @chat independently
export default function SupportLayout({ tickets, chat }: {
  tickets: React.ReactNode; chat: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <aside>{tickets}</aside>
      <main>{chat}</main>
    </div>
  );
}
// Directories: app/support/@tickets/page.tsx  app/support/@chat/page.tsx
// Use case: dashboards, live feeds, multi-pane UIs loading at different speeds
```

---

## Data Fetching

### ISR Revalidation Guidelines

| Content Type | Revalidate | Pattern |
|---|---|---|
| Blog / docs | 60s | `next: { revalidate: 60 }` |
| News feed | 10s | `next: { revalidate: 10 }` |
| Products / pricing | 300s | `next: { revalidate: 300 }` |
| Static marketing | 86400s | `cache: 'force-cache'` |
| User-specific | Dynamic | `cache: 'no-store'` |
| Real-time (stock) | N/A | SSR or WebSocket |

### Parallel Fetch + React cache()

```tsx
// Parallel fetching
const [user, posts] = await Promise.all([
  fetch('/api/user').then(r => r.json()),
  fetch('/api/posts').then(r => r.json()),
]);

// Deduplication for POST/GraphQL requests
import { cache } from 'react';
export const getUser = cache(async (id: string) => db.user.findUnique({ where: { id } }));
```

---

## Route Handlers (API Routes)

Route Handlers are public entry points. Authenticate and authorize in the
data-access function on every request; never return an unscoped table scan. See
`references/tenant-data-security.md` for the complete read-only example.

---

## Server Actions

Treat each Server Action as a public endpoint: authenticate, authorize,
validate, mutate, then revalidate only the affected path or tag. Do not rely on
a hidden UI control or page-level check for authorization.

### Server Actions vs API Routes

| Use | When |
|---|---|
| Server Action | Form submissions, mutations from UI, same-app data changes |
| API Route | Public APIs, webhooks, third-party consumers, complex error handling |

---

## Proxy and request routing

```ts
// proxy.ts — project root. A redirect is only a navigation aid.
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSessionCookie = Boolean(request.cookies.get('session')?.value);
  if (!hasSessionCookie && pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*', '/api/:path*'] };
```

---

## Authorization and tenant data access

```ts
Proxy may perform an optimistic redirect from the presence of a session cookie.
It must not trust a role cookie, establish tenant membership, or replace a
server-side authorization check. Verify the session and permission in a
server-only data-access layer for each page, Route Handler, and Server Action.
Apply the verified tenant predicate in the database query and return an
allowlisted DTO. See `references/tenant-data-security.md` for a complete
read-only invoice path and negative cases.
```

---

## Redis Caching

```ts
// lib/redis.ts
import Redis from 'ioredis';
const redis = new Redis(process.env.REDIS_URL!);
export default redis;

User-specific results must not use a shared cache key or a shared static
render. Establish authorization before reading data. If a cache is introduced,
prove key isolation, invalidation, expiry, and failure behaviour for the
verified tenant and permission context; otherwise keep the path uncached and
private. Cache invalidation is not an authorization control.
```

---

## Background Jobs (BullMQ)

```ts
// lib/queue.ts
import { Queue, Worker } from 'bullmq';
import Redis from 'ioredis';
const connection = new Redis(process.env.REDIS_URL!);
export const emailQueue = new Queue('email', { connection });

// Worker (separate process or dedicated route)
new Worker('email', async (job) => {
  const { to, subject, body } = job.data;
  await sendEmail(to, subject, body);
}, { connection });

// Enqueue from API route
export async function POST(req: NextRequest) {
  const { email } = await req.json();
  await emailQueue.add('welcome', { to: email, subject: 'Welcome!' });
  return Response.json({ queued: true });
}
```

---

## Authentication (NextAuth v5)

```ts
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [GitHub({ clientId: process.env.GITHUB_ID!, clientSecret: process.env.GITHUB_SECRET! })],
  callbacks: {
    jwt({ token, user }) { if (user) token.role = user.role; return token; },
    session({ session, token }) { session.user.role = token.role as string; return session; },
  },
});
```

---

## Database (Prisma Singleton)

```ts
// lib/prisma.ts — prevents connection exhaustion in dev HMR
import { PrismaClient } from '@prisma/client';
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
export const db = globalForPrisma.prisma || new PrismaClient({ log: ['query'] });
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
```

### Database Selection

| Database | Use When |
|---|---|
| PostgreSQL + Prisma | Relational data, transactions, production default |
| MongoDB + Mongoose | Document/flexible schemas, content management |
| Firebase Firestore | Real-time sync, serverless, mobile-first |

---

## CI/CD (GitHub Actions)

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with: { node-version: '24.x' }
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - run: npm install -g vercel && vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## Deployment

| Platform | Best For |
|---|---|
| **Vercel** | Zero-config, global CDN, Edge Network, native Next.js |
| **Railway** | Simple self-hosted, easy DB provisioning |
| **AWS Amplify** | Full AWS ecosystem, enterprise |
| **Docker/Self-hosted** | Full control, no vendor lock-in |

```dockerfile
# next.config.js: module.exports = { output: 'standalone' }
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
CMD ["node", "server.js"]
```

---

## Built-in Components

```tsx
import Image from 'next/image';
import Link from 'next/link';

<Image src="/hero.jpg" alt="Hero" width={800} height={600} priority />
<Link href="/dashboard">Dashboard</Link>
<Link href={`/blog/${slug}`} prefetch={false}>Post</Link>
```

---

## Anti-Patterns

- Do NOT `'use client'` every component — server by default
- Do NOT use `getServerSideProps`/`getStaticProps` in App Router
- Do NOT store secrets in `NEXT_PUBLIC_` vars
- Do NOT `useEffect` for data — fetch in server components
- Do NOT create separate Express servers — use Route Handlers
- Do NOT await fetches sequentially — use `Promise.all`
- Do NOT skip `loading.tsx` — every dynamic route needs a Suspense boundary

---

*Sources: Rambert — Advanced Next.js for Everyone (2024); Kim — The Next.js Handbook (2023); Jain — Modern Web Applications with Next.js (2024); Krause — The Complete Developer (2024)*

## Decision rules

| Condition | Choice | Failure avoided |
|---|---|---|
| No browser API or interaction is needed | Keep a Server Component | Unnecessary client JavaScript |
| Independent data blocks a route | Fetch concurrently and stream non-critical regions | Sequential latency |
| Mutation is application-internal | Use a validated, authorised Server Action | Duplicate transport plumbing |
| Contract serves external consumers | Use a Route Handler with an explicit contract | Hidden coupling |

## Capability contract

Read and search the application first. Edit only when authorised; execute the existing type-check, tests, build, and route smoke checks when available. Network access is optional for current Next.js documentation.
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| Next.js version, route requirements, data/cache boundaries, auth, and deployment target | yes | Select App Router patterns |
## Outputs
- Produce Next.js implementation or design with route, cache, error, test, and deployment evidence.
## Degraded mode
Fallback without a runnable Next.js environment: provide route/cache contracts and mark runtime rendering and invalidation unverified.
