import 'server-only';
import { auth } from '@/auth';
import { db } from '@/lib/db';

export class UnauthenticatedError extends Error {}
export class ForbiddenError extends Error {}

export type InvoiceDto = {
  id: string;
  number: string;
  currency: string;
  // Serialize BIGINT minor units as decimal text to avoid JS precision loss.
  amountMinor: string;
  customer: string;
};

export type ParsedInvoiceQuery = { search: string; limit: number };

export function parseInvoiceListQuery(
  searches: string[],
  limits: string[],
): ParsedInvoiceQuery | null {
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
  if (search.length > 120 || !Number.isSafeInteger(limit) || limit < 1 || limit > 100) {
    throw new RangeError('Invalid invoice-list query');
  }
  const session = await auth();
  if (!session?.user?.id || !session.user.tenantId) {
    throw new UnauthenticatedError();
  }

  // Replace these illustrative names with the application's schema. Confirm
  // membership and permission from server-owned data, not a role/tenant cookie.
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
      id: row.id.toString(),
      number: row.number,
      currency: row.currency,
      amountMinor: row.amountMinor.toString(),
      customer: row.customer.name,
    };
  });
}
