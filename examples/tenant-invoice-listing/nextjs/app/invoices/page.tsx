import { redirect } from 'next/navigation';
import type { InvoiceDto } from '@/lib/invoices';
import {
  ForbiddenError,
  UnauthenticatedError,
  listInvoicesForCurrentTenant,
} from '@/lib/invoices';

type PageProps = {
  searchParams: Promise<{ q?: string; limit?: string }>;
};

export const dynamic = 'force-dynamic';

export default async function InvoicesPage({ searchParams }: PageProps) {
  const query = await searchParams;
  const search = (query.q ?? '').slice(0, 120);
  const requestedLimit = Number(query.limit ?? 20);
  const limit = Number.isInteger(requestedLimit)
    ? Math.max(1, Math.min(requestedLimit, 100))
    : 20;
  let invoices: InvoiceDto[];
  try {
    invoices = await listInvoicesForCurrentTenant(search, limit);
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
