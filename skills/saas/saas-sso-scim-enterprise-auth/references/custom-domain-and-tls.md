# Custom Domain and Automated TLS (Reference)

Deep-dive for `saas-sso-scim-enterprise-auth` section 6. Covers DNS verification,
CNAME / ACME certificate issuance, automated renewal, SNI-based routing, and the
fingerprint / ownership checks that stop a tenant pointing a domain they do not
control at your platform.

Goal: a tenant logs in at `app.acme.com` instead of `acme.your-saas.com`, with a
valid TLS cert your platform provisions and renews automatically, routed to the
right tenant with no shared secret in the app.

## End-to-end flow

```text
1. Tenant admin enters custom hostname: app.acme.com
2. Platform shows TWO records to add at the tenant's DNS:
     a) CNAME  app.acme.com           -> tenant-acme.cname.your-saas.com   (routing)
     b) TXT    _saas-verify.acme.com  -> saas-verify=<random-32-byte-token> (ownership)
3. Tenant adds both records
4. Platform polls DNS until BOTH resolve correctly (ownership + routing)
5. Platform requests an ACME cert (HTTP-01 or DNS-01) for app.acme.com
6. Cert issued + installed at the edge; domain marked active for tenant-acme
7. Edge terminates TLS using SNI, resolves hostname -> tenant, injects X-Tenant-Id
8. Cert auto-renews ~30 days before expiry; renewal failure pages on-call
```

Separate the two concerns. The CNAME is for routing. The TXT (or a separate
delegated CNAME for DNS-01) proves ownership. Do not infer ownership from the
routing CNAME alone -- see the takeover failure mode below.

## DNS verification: prove ownership before issuing

| Method | Record | Pros | Cons |
|---|---|---|---|
| TXT token | `_saas-verify.acme.com TXT saas-verify=<token>` | Simple; works with any DNS | Extra record; tenant must keep it |
| HTTP-01 ACME | none (served at `/.well-known/acme-challenge/`) | No DNS round-trip for proof | Needs the CNAME already live |
| DNS-01 ACME | `_acme-challenge.acme.com CNAME ...` (delegated) | Supports wildcards; no inbound HTTP | Tenant delegates a subdomain to you |

Recommended default: TXT token for ownership + HTTP-01 for issuance once the
CNAME is live. Use DNS-01 only if you need wildcard certs or the tenant cannot
expose HTTP-01.

Polling logic:

```text
verify_domain(hostname, expected_target, txt_token):
  txt = resolve_TXT("_saas-verify." + root_of(hostname))
  if ("saas-verify=" + txt_token) not in txt:
      return PENDING_OWNERSHIP        # do NOT issue a cert yet
  cname = resolve_CNAME(hostname)
  if cname != expected_target:
      return PENDING_ROUTING
  return VERIFIED
```

Poll with backoff (e.g. every 30s for 10 min, then every 5 min for 24h), then
give up with a clear error. Cache negative results so you do not hammer DNS.

## Certificate issuance via ACME

Use cert-manager (Kubernetes), Caddy, an ACME client (Certbot / lego / acme.sh),
or a managed CDN that does ACME for you (Cloudflare for SaaS, Fastly, AWS ACM via
CloudFront custom domains).

| Issuance path | Validation | Best for | Failure mode if misused |
|---|---|---|---|
| HTTP-01 | Serve token at `/.well-known/acme-challenge/<t>` | Single hostname, CNAME live | Fails if edge does not yet route the host |
| DNS-01 | Publish `_acme-challenge` TXT | Wildcards, no inbound HTTP | Slow propagation; needs DNS API or delegation |
| TLS-ALPN-01 | TLS handshake on port 443 | Edge controls 443 fully | Needs ALPN support at the terminator |

HTTP-01 chicken-and-egg: the ACME server fetches the challenge over HTTP at the
custom hostname, which only resolves to you once the CNAME is live. So order is:
verify CNAME resolves -> then request HTTP-01. If you request first you get a
spurious failure.

cert-manager per-tenant Certificate (illustrative):

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cd-tenant-acme
  namespace: ingress
spec:
  secretName: tls-tenant-acme
  dnsNames: ["app.acme.com"]
  issuerRef: { name: letsencrypt-prod, kind: ClusterIssuer }
  renewBefore: 720h   # 30 days
```

## Renewal and operations

- Renew at ~30 days remaining. Let's Encrypt certs are 90 days; never wait until
  expiry.
- Renewal failure is a paging alert, not a log line. An expired cert on a custom
  domain is a visible outage for that tenant.
- Track per-tenant cert state: issued / renewing / failed / expired. Surface it
  in the tenant admin UI so they see "active" vs "DNS not yet propagated".
- Rate limits: Let's Encrypt caps certs per registered domain per week. At scale
  use a CA without punishing limits, batch with SAN certs where appropriate, or
  use a managed CDN that pools issuance.
- Revoke and clean up the cert when a tenant removes the custom domain or
  offboards, so stale certs do not linger.

## SNI-based routing at the edge

The edge terminates TLS. During the handshake the client sends SNI (the
hostname); the edge selects the matching cert, then resolves hostname -> tenant
and forwards to the backend with a trusted header.

```text
TLS ClientHello (SNI = app.acme.com)
  -> edge selects tls-tenant-acme cert
  -> edge looks up hostname in routing table -> tenant-acme
  -> edge proxies to backend with header X-Tenant-Id: acme  (set BY the edge)
backend trusts X-Tenant-Id ONLY because it arrived from the trusted edge
```

The backend MUST NOT trust `X-Tenant-Id` from arbitrary clients. Strip and
re-set it at the edge so a client cannot forge it. Bind the listener so the only
path to the backend is through the edge (private network / mTLS between edge and
backend), otherwise an attacker bypasses the edge and forges the tenant header.

Nginx sketch:

```nginx
server {
    listen 443 ssl;
    server_name app.acme.com;
    ssl_certificate     /etc/certs/tenant-acme/fullchain.pem;
    ssl_certificate_key /etc/certs/tenant-acme/privkey.pem;
    location / {
        proxy_set_header X-Tenant-Id "acme";   # edge sets it; client value discarded
        proxy_pass http://backend_pool;
    }
}
```

## Fingerprint / ownership validation (anti-takeover)

The classic subdomain-takeover scenario: a tenant adds the routing CNAME, later
deletes their DNS zone or removes the CNAME, but you keep serving the cert and
routing. Or an attacker registers `evil.example` pointing at your CNAME target
without ever owning it. Defences:

- Require the TXT ownership proof to remain present; re-verify periodically (not
  just once at setup). If it disappears, deactivate the domain.
- Pin the expected CNAME target; if the CNAME no longer points at you, stop
  serving and revoke the cert.
- Never auto-issue a cert for a hostname whose ownership TXT does not currently
  validate. Failure mode of skipping re-verification: a dangling custom domain
  becomes an attacker-controlled login page on your TLS infrastructure.

## Apex / root domain note

A bare apex (`acme.com`, no subdomain) cannot use a CNAME (DNS rules forbid CNAME
at apex alongside other records). Options: ALIAS/ANAME records (Route 53, NS1,
Cloudflare), or ask the tenant to use a subdomain (`app.acme.com`). Default:
require a subdomain; document apex as advanced.

## Decision table: who issues the cert

| Situation | Choose | Why |
|---|---|---|
| Already on Cloudflare | Cloudflare for SaaS | Custom hostnames + ACME managed for you |
| Kubernetes ingress | cert-manager + ClusterIssuer | Native, declarative renewal |
| Few custom domains, VMs | Caddy or Certbot + cron | Lowest moving parts |
| Thousands of domains | Managed CDN / SaaS hostname product | You will hit CA rate limits otherwise |

## Anti-patterns

- Issuing a cert before the ownership TXT validates.
- Treating the routing CNAME as proof of ownership.
- Trusting `X-Tenant-Id` from the client instead of setting it at the edge.
- Backend reachable bypassing the edge (header can then be forged).
- One-time verification with no periodic re-check (dangling-domain takeover).
- Renewing at expiry instead of ~30 days out (guaranteed periodic outages).
