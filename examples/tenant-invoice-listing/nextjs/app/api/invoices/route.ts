import { NextResponse } from 'next/server';
import {
  ForbiddenError,
  parseInvoiceListQuery,
  UnauthenticatedError,
  listInvoicesForCurrentTenant,
} from '@/lib/invoices';

export async function GET(request: Request) {
  const url = new URL(request.url);
  const parsed = parseInvoiceListQuery(
    url.searchParams.getAll('q'),
    url.searchParams.getAll('limit'),
  );
  if (!parsed) {
    return NextResponse.json({ error: 'Invalid listing input' }, { status: 400 });
  }

  try {
    const data = await listInvoicesForCurrentTenant(parsed.search, parsed.limit);
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
