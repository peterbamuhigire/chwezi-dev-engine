import { redirect } from 'next/navigation';
import type { InvoiceDto } from '@/lib/invoices';
import {
  ForbiddenError,
  parseInvoiceListQuery,
  UnauthenticatedError,
  listInvoicesForCurrentTenant,
} from '@/lib/invoices';

type PageProps = {
  searchParams: Promise<{ q?: string | string[]; limit?: string | string[] }>;
};

export const dynamic = 'force-dynamic';

export default async function InvoicesPage({ searchParams }: PageProps) {
  const query = await searchParams;
  const parsed = parseInvoiceListQuery(
    query.q === undefined ? [] : Array.isArray(query.q) ? query.q : [query.q],
    query.limit === undefined ? [] : Array.isArray(query.limit) ? query.limit : [query.limit],
  );
  if (!parsed) {
    return <main><h1>Invoices</h1><p role="alert">Invalid invoice-list query.</p></main>;
  }
  let invoices: InvoiceDto[];
  try {
    invoices = await listInvoicesForCurrentTenant(parsed.search, parsed.limit);
  } catch (error) {
    if (error instanceof UnauthenticatedError) redirect('/login');
    if (error instanceof ForbiddenError) {
      return <p role="status">You do not have access to invoices.</p>;
    }
    throw error;
  }

  return (
    <main>
      <h1>Invoices</h1>
      {invoices.length === 0 ? (
        <p role="status">No invoices found.</p>
      ) : (
        <table>
          <caption>Invoices</caption>
          <thead><tr><th scope="col">Number</th><th scope="col">Customer</th><th scope="col">Currency</th><th scope="col">Amount in minor units</th></tr></thead>
          <tbody>{invoices.map((invoice) => (
            <tr key={invoice.id}>
              <td>{invoice.number}</td><td>{invoice.customer}</td>
              <td>{invoice.currency}</td><td>{invoice.amountMinor}</td>
            </tr>
          ))}</tbody>
        </table>
      )}
    </main>
  );
}
