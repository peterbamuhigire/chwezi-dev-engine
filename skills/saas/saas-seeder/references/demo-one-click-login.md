# Demo one-click login standard (no passwords anywhere)

Standard for every SaaS demo environment built from this engine. Adopted 28 Sep
2026 from the Maduuka implementation (`sign-in.php`, `App\Auth\Demo\DemoLoginPolicy`,
`AuthService::authenticateDemoUser()`).

## Rules

1. **No password in git, pages or docs.** Demo passwords never appear in source,
   HTML/JS, seed scripts, tests, evidence files, READMEs or commit messages. Scripts
   and tests that need one read it from the environment (for example
   `APP_DEMO_PASSWORD` in an untracked `.env`). A pre-commit hook refuses staged
   lines that pair the known demo password with `pass`/`password`.
2. **Buttons are the only door on a demo host.** On a demo host the sign-in page
   shows one button per demo profile (for example Pharmacy, Supermarket,
   Restaurant) and no username/password form. The server refuses password posts
   on a demo host, so the form cannot be restored by editing the page.
3. **The button posts a profile key, never a credential.** The request carries
   `demo_profile=<key>` plus the normal CSRF token. The server maps the key
   through a code-owned allow-list to a demo username. Unknown keys are refused
   with a plain message.
4. **Same RBAC as a real sign-in.** The server signs the mapped user in through
   the same authentication service and session setup as a password login, skipping
   only the password comparison. Account status, organisation status, locks,
   subscription state, second factor (if enabled), session regeneration, rate
   limiting, CSRF and audit logging all still apply. The visitor gets exactly that
   user's roles and permissions.
5. **Three gates, all required.**
   - `DEMO_LOGIN_ENABLED=true` in that server's untracked `.env` (off by default).
   - The request host is a demo host: it contains `demo`, or is listed in
     `DEMO_LOGIN_HOSTS` (comma separated; use for local QA only).
   - The profile key is on the allow-list.
   A demo host with the flag off shows a plain "demo sign-in is switched off"
   notice instead of dead buttons.
6. **Audited.** Each demo sign-in writes an `auth` log line marked "demo login"
   with the profile key and username.
7. **Demo accounts are ordinary accounts.** Their passwords exist only as hashes
   in the database, so they can be rotated at any time without touching code. Never
   seed a production tenant with a demo profile, and never map a profile to a
   super-admin or platform-operator account.

## Reference implementation shape (PHP)

```php
final class DemoLoginPolicy
{
    public const DEFAULT_PROFILES = ['pharmacy' => 'johndoe', 'restaurant' => 'restaurant'];

    public static function fromEnvironment(): self;          // DEMO_LOGIN_ENABLED, DEMO_LOGIN_HOSTS
    public function isDemoHost(string $host): bool;          // UI: buttons instead of form
    public function allows(string $host): bool;              // enabled && demo host
    public function usernameFor(string $profile): ?string;   // allow-list lookup
}

// AuthService: one private runAuthentication(LoginDTO $c, bool $checkPassword)
// behind two public entry points so every non-password check is shared.
public function authenticate(LoginDTO $c): AuthResult { return $this->runAuthentication($c, true); }
public function authenticateDemoUser(string $username, ?string $ip, ?string $ua = null): AuthResult
{
    return $this->runAuthentication(new LoginDTO($username, '', $ip, $ua), false);
}
```

Sign-in controller on a demo host: refuse unless `allows($host)`; resolve
`usernameFor($_POST['demo_profile'])`; call `authenticateDemoUser()`; then run the
exact same post-authentication session code as a password login (no "remember me").

## Verification checklist

- [ ] Unit tests: disabled policy never allows; only demo hosts allowed; extra
      hosts honoured; only allow-listed keys map; environment default is off.
- [ ] HTTP on a demo host: page has buttons and no password field; each button
      reaches the dashboard as that user; unknown profile refused; username/password
      post refused.
- [ ] HTTP on a non-demo host: normal form, no demo buttons.
- [ ] Permissions of the demo session equal those of a password sign-in for the
      same user (compare the loaded permission set).
- [ ] `git grep` for the demo password in pairs with `password` returns nothing;
      the pre-commit hook blocks a test commit that adds one.
- [ ] Production `.env` has `DEMO_LOGIN_ENABLED` unset or `false`.

## Anti-patterns

- Filling a hidden password field from JavaScript (the password is public in page
  source and in git).
- Printing the password from `.env` into the page (out of git, still public).
- A separate "demo session" code path that builds `$_SESSION` by hand (drifts from
  real RBAC, skips status and subscription checks).
- Mapping a demo button to an administrator account.
- Documenting demo credentials in READMEs, runbooks or test evidence.
