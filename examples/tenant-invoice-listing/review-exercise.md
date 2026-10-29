# Manual review exercise: unsafe invoice listing

This is a deliberately flawed, synthetic specimen copied from the pre-change
practitioner observation. **Do not run or deploy it.** The review below groups the
observed defects into four findings so a practitioner can compare their review with the
expected result.

```php
$rows = $db->query("SELECT * FROM invoices WHERE number LIKE '%" . $_GET['q'] . "%'");
foreach ($rows as $row) {
    $customer = $db->query("SELECT name FROM customers WHERE id=" . $row['customer_id'])->fetch();
    echo $customer['name'];
}
$db->exec("INSERT INTO journal_lines(account_id, amount) VALUES (1, 100)");
```

## Expected review

1. **Untrusted and unscoped invoice query:** the search is interpolated into SQL, and the
   query has no verified tenant predicate. Use a bound value and derive tenant identity
   from the authenticated server context.
2. **N+1 and unscoped customer lookup:** the code queries once per invoice and looks up a
   customer by ID without verifying that customer belongs to the invoice tenant. Use one
   tenant-scoped join with an allowlisted display DTO and bounded page size.
3. **Unescaped output:** a customer name is emitted as HTML without context-appropriate
   escaping. Escape rendered text and keep semantic table headings.
4. **Ledger mutation in a read path:** the listing writes a journal line directly, outside
   the doctrine-controlled `JournalPostingService` and without its authorised balanced
   transaction boundary. Remove posting from the read path; any separate posting flow
   must route through that service.

This is a manual practitioner review, not a model benchmark or proof that routing detects
these vulnerabilities. The corrected teaching slice is in the neighboring PHP example;
it deliberately performs no journal write.
