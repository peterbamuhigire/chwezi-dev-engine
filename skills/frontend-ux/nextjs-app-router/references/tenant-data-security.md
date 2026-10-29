# Tenant-scoped server data in Next.js

**Evidence date:** 2026-10-29. **Scope:** read-only App Router examples for a tenant-owned invoice list. These patterns do not replace the application's verified identity provider, schema, database constraints, threat model, or release tests.

Next.js recommends a server-only data-access layer (DAL), DTOs, and authorization checks at sensitive data boundaries. Proxy checks are optional and should remain optimistic; Server Actions and Route Handlers require their own authorization checks. Read the current Next.js authentication and security guides before adapting this reference.

## Server-only data access

```ts
import 'server-only';
import { auth } from '@/auth';
import { db } from '@/lib/db';

export class UnauthenticatedError extends Error {}
export class ForbiddenError extends Error {}

export type InvoiceDto = {
  id: string;
  number: string;
  currency: string;
  amountMinor: string;
  customer: string;
};

export function parseInvoiceListQuery(searches: string[], limits: string[]) {
  if (searches.length > 1 || limits.length > 1) return null;
  const search = searches[0] ?? '';
  if (search.length > 120) return null;
  const rawLimit = limits[0];
  if (rawLimit === undefined) return { search, limit: 20 };
  if (!/^\d+$/.test(rawLimit)) return null;
  const limit = Number(rawLimit);
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 100) return null;
  return { search, limit };
}

export async function listInvoicesForCurrentTenant(
  search: string,
  limit: number,
): Promise<InvoiceDto[]> {
  const session = await auth();
  if (!session?.user?.id || !session.user.tenantId) {
    throw new UnauthenticatedError();
  }

  // Replace field names with the application's schema. Confirm membership and
  // permission from server-owned data; a role/tenant cookie is not authority.
  const membership = await db.tenantMembership.findFirst({
    where: {
      userId: session.user.id,
      tenantId: session.user.tenantId,
      status: 'ACTIVE',
      permissions: { some: { name: 'invoice:read' } },
    },
    select: { tenantId: true },
  });
  if (!membership) throw new ForbiddenError();

  const rows = await db.invoice.findMany({
    where: {
      tenantId: membership.tenantId,
      number: { contains: search },
    },
    select: {
      id: true,
      number: true,
      currency: true,
      amountMinor: true,
      customer: { select: { name: true, tenantId: true } },
    },
    orderBy: { id: 'asc' },
    take: limit,
  });

  return rows.map((row) => {
    if (row.customer.tenantId !== membership.tenantId) {
      throw new Error('Invoice/customer tenant integrity failure');
    }
    return {
      // Prisma BigInt values are not JSON-safe and can exceed JS safe integers.
      id: row.id.toString(),
      number: row.number,
      currency: row.currency,
      amountMinor: row.amountMinor.toString(),
      customer: row.customer.name,
    };
  });
}
```

The illustrative ORM relation shape must be aligned with the actual schema. Keep a database constraint joining invoice and customer ownership where the database supports it. Bound user input before calling the DAL. The DAL returns only display fields and does not perform a ledger write.

## Page and route handler

In Next.js 16, `params`, `searchParams`, `cookies()`, and `headers()` are asynchronous request APIs. User-specific pages must render from request-time data and must not enter a shared static cache. The version-16 guide and file-convention reference should be checked before upgrading or changing a route.

```tsx
// app/invoices/page.tsx
import { redirect } from 'next/navigation';
import {
  ForbiddenError,
  UnauthenticatedError,
  listInvoicesForCurrentTenant,
  parseInvoiceListQuery,
} from '@/lib/invoices';

type PageProps = { searchParams: Promise<{ q?: string | string[]; limit?: string | string[] }> };
export const dynamic = 'force-dynamic';

export default async function InvoicesPage({ searchParams }: PageProps) {
  const query = await searchParams;
  const parsed = parseInvoiceListQuery(
    query.q === undefined ? [] : Array.isArray(query.q) ? query.q : [query.q],
    query.limit === undefined ? [] : Array.isArray(query.limit) ? query.limit : [query.limit],
  );
  if (!parsed) return <p role="alert">Invalid invoice-list query.</p>;
  try {
    const invoices = await listInvoicesForCurrentTenant(parsed.search, parsed.limit);
    return <InvoiceTable invoices={invoices} />;
  } catch (error) {
    if (error instanceof UnauthenticatedError) redirect('/login');
    if (error instanceof ForbiddenError) return <p role="status">You do not have access to invoices.</p>;
    throw error;
  }
}
```

`InvoiceTable` above is the application's accessible table component; provide it in the project and test its empty and loading states. A Route Handler should parse and bound query parameters before calling the same DAL, map invalid/unauthenticated/forbidden failures to 400/401/403, and set `Cache-Control: private, no-store`. It must not accept a tenant identifier as authority from query, body, header, or an unsigned cookie.

## Proxy boundary

Use `proxy.ts` for optional fast navigation redirects only. A cookie-presence check can improve navigation but does not prove identity, role, permission, or current tenant membership. Keep all decisive checks in the DAL or mutation handler.

## Cache decision

Do not cache tenant-owned results globally. If the product later needs a cache, prove that authorization precedes lookup and that the key includes every access-control dimension; test cross-tenant collisions, membership revocation, invalidation, expiry, and cache failure. Until then use a private uncached path.

## Review negatives

Reject these implementations:

- trust `request.cookies.get('role')` as a permission decision;
- read `db.user.findMany()` or another private table without a verified tenant predicate;
- cache private results under a global key such as `users`;
- assume a page or Proxy check protects a Route Handler or Server Action;
- use synchronous page `params`/`searchParams` in Next.js 16;
- use removed `request.ip` or `request.geo` properties as current APIs;
- perform mutations from a read-only listing route.

## Source register

- Next.js Authentication Guide: <https://nextjs.org/docs/app/guides/authentication> (official, accessed 2026-10-29; current page revision shown as 2026-03-25).
- Next.js Data Security Guide: <https://nextjs.org/docs/app/guides/data-security> (official, accessed 2026-10-29).
- Next.js Version 16 Upgrade Guide: <https://nextjs.org/docs/app/guides/upgrading/version-16> (official, accessed 2026-10-29).
- Proxy convention: <https://nextjs.org/docs/app/api-reference/file-conventions/proxy> (official, accessed 2026-10-29).
- Security applicability is recorded in `docs/source-registers/skills-engine-currentness-2026-09.json`; source currency does not certify a deployed application.
