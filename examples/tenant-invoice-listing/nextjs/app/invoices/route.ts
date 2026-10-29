import { NextResponse } from 'next/server';
import {
  ForbiddenError,
  UnauthenticatedError,
  listInvoicesForCurrentTenant,
} from '@/lib/invoices';

export async function GET(request: Request) {
  const url = new URL(request.url);
  const search = (url.searchParams.get('q') ?? '').slice(0, 120);
  const rawLimit = Number(url.searchParams.get('limit') ?? 20);
  const limit = Number.isInteger(rawLimit) ? Math.max(1, Math.min(rawLimit, 100)) : 20;

  try {
    const data = await listInvoicesForCurrentTenant(search, limit);
    return NextResponse.json({ data }, {
      headers: { 'Cache-Control': 'private, no-store' },
    });
  } catch (error) {
    if (error instanceof ForbiddenError) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }
    if (error instanceof UnauthenticatedError) {
      return NextResponse.json({ error: 'Unauthenticated' }, { status: 401 });
    }
    throw error;
  }
}
