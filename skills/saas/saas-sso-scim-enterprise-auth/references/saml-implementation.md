# SAML 2.0 Implementation (Reference)

Deep-dive for `saas-sso-scim-enterprise-auth` section 4. Covers SP/IdP metadata, the
ACS contract, signing and encryption, JIT provisioning, and the validation
pitfalls that turn into CVEs when you get them wrong.

Default position: do not hand-roll the XML signature layer. Use a vetted
library (`python3-saml`, `samlify`, `crewjam/saml`, `onelogin/php-saml`) or buy
(WorkOS, Auth0). This reference explains what that library does so you can
configure it correctly and debug it when the IdP integration fails.

## Roles and the two metadata documents

| Role | You are | They are | Document they consume |
|---|---|---|---|
| Service Provider (SP) | Your SaaS | The buyer | Your SP metadata |
| Identity Provider (IdP) | Okta / Azure AD / Ping | The buyer | Their IdP metadata |

SAML is a metadata exchange. Both sides publish an XML document describing their
entity ID, endpoints, and signing certificates. You generate yours per tenant;
they paste theirs (XML or a metadata URL) into your tenant IdP config.

### Your SP metadata (served at `GET /sso/saml/{tenant}/metadata`)

```xml
<EntityDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
                  entityID="https://app.example.com/sso/saml/acme">
  <SPSSODescriptor AuthnRequestsSigned="true"
                   WantAssertionsSigned="true"
                   protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <KeyDescriptor use="signing">
      <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
        <X509Data><X509Certificate>MIID...your SP signing cert...</X509Certificate></X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <KeyDescriptor use="encryption">
      <KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
        <X509Data><X509Certificate>MIID...your SP encryption cert...</X509Certificate></X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                         Location="https://app.example.com/sso/saml/acme/sls"/>
    <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</NameIDFormat>
    <AssertionConsumerService index="0" isDefault="true"
                              Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                              Location="https://app.example.com/sso/saml/acme/acs"/>
  </SPSSODescriptor>
</EntityDescriptor>
```

The `entityID` is your stable identifier; it MUST be tenant-unique so that one
tenant's assertion can never be replayed at another tenant's ACS. Use a path or
query that includes the tenant slug. Never use a single global entity ID across
all tenants.

## The flow, end to end (SP-initiated)

```text
1. User hits app, enters work email -> resolve email domain -> tenant
2. SP builds <AuthnRequest>, signs it (if AuthnRequestsSigned), redirects (HTTP-Redirect)
   to tenant.saml_sso_url with ?SAMLRequest=<deflate+base64>&RelayState=<opaque>
3. IdP authenticates the user (password + MFA, on the IdP side)
4. IdP POSTs <Response> (HTTP-POST binding) to your ACS:
   POST /sso/saml/acme/acs  body: SAMLResponse=<base64>&RelayState=<opaque>
5. SP validates (see checklist), extracts attributes, JIT-provisions, issues session
6. SP redirects to the RelayState target (the deep link the user started from)
```

IdP-initiated flow skips steps 1-3: the user clicks the app tile in their IdP
dashboard and the IdP POSTs an unsolicited `<Response>` to your ACS with no
`InResponseTo`. Support it only if a customer needs it, and treat unsolicited
responses with extra suspicion (no request to correlate against).

## The ACS validation checklist (the security-critical part)

Validate IN THIS ORDER and reject on the first failure. Each line names the
attack the check prevents.

```text
[ ] XML parses with DTD loading and external entities DISABLED   -> prevents XXE / billion-laughs
[ ] Signature present on Response OR every Assertion              -> prevents unsigned forgery
[ ] Signature verifies against the tenant's CONFIGURED cert       -> prevents attacker-supplied key
[ ] The signed element is the one you consume (canonical ref)     -> prevents XML Signature Wrapping
[ ] Issuer == tenant.saml_entity_id                               -> prevents cross-IdP confusion
[ ] Audience == your SP entityID for THIS tenant                  -> prevents cross-tenant replay
[ ] Recipient (in SubjectConfirmationData) == your ACS URL        -> prevents token redirection
[ ] NotBefore <= now <= NotOnOrAfter (small clock skew, e.g. 60s) -> prevents expired/early assertions
[ ] InResponseTo matches a request you issued (SP-initiated only) -> prevents response injection
[ ] Assertion ID not seen before within validity window          -> prevents replay
[ ] StatusCode == urn:oasis:names:tc:SAML:2.0:status:Success      -> reject AuthnFailed etc.
```

### XML Signature Wrapping (XSW) -- the canonical pitfall

The attack: the response contains a validly signed assertion AND a second,
attacker-controlled assertion. A naive verifier checks "is there a valid
signature somewhere?" (yes) and then reads attributes from the WRONG element.
Failure mode: full account takeover -- the attacker authenticates as any user.

Defence: verify the signature, then read attributes ONLY from the exact element
the signature reference points at. Reject documents with more assertions than
expected. This is precisely why you use a hardened library and keep it patched;
roll-your-own DOM walking is where teams ship XSW bugs.

### XXE / entity expansion

Parse with a hardened parser. In Python lxml:

```python
from lxml import etree

parser = etree.XMLParser(
    resolve_entities=False,   # no external entity resolution -> no XXE
    no_network=True,          # never fetch a remote DTD
    huge_tree=False,          # bound expansion -> no billion-laughs DoS
    dtd_validation=False,
    load_dtd=False,
)
doc = etree.fromstring(saml_response_bytes, parser)
```

Failure mode of skipping this: a single crafted assertion reads local files
(`/etc/passwd`) or hangs the worker (billion-laughs DoS).

## Signing and encryption decision table

| Concern | Setting | When to require it | Failure mode if wrong |
|---|---|---|---|
| Sign AuthnRequest | `AuthnRequestsSigned=true` | When IdP requires it (Azure can) | IdP rejects request; login loops |
| Sign Response/Assertion | always require one | Always | Forged assertions accepted |
| Encrypt Assertion | `WantAssertionsEncrypted` | If attributes contain PII in transit beyond TLS | Attributes leak in logs/proxies |
| Sign SLO LogoutRequest | required by most IdPs | When supporting SLO | Logout silently ignored |

You always want at least: signed assertion + verified against the configured
cert. Encryption is optional (TLS already protects the wire) but some buyers
mandate it; support it but do not require it by default.

## Attribute mapping and JIT provisioning

The IdP sends attributes in an `<AttributeStatement>`. Map them via the
per-tenant config (`saml_attr_email`, `saml_attr_name`, `saml_attr_groups`).

```python
EMAIL = attrs.get(cfg.saml_attr_email) or assertion.subject.name_id  # fall back to NameID
NAME  = attrs.get(cfg.saml_attr_name, "")
GROUPS = attrs.get(cfg.saml_attr_groups, [])  # often a list

def jit_provision(tenant, email, name, idp_groups, cfg):
    # 1. Domain guard: the asserted email MUST be in the tenant's verified domain.
    if not cfg.domain_verified or not email.lower().endswith("@" + cfg.email_domain):
        raise SamlReject("email domain not claimed by tenant")  # prevents tenant takeover
    # 2. Resolve user (match on normalised email within the tenant, never globally).
    user = find_user(tenant.id, email) or create_user(tenant.id, email, name)
    # 3. Map IdP groups to platform roles via cfg.scim_group_mapping / saml mapping.
    roles = {cfg.group_mapping[g] for g in idp_groups if g in cfg.group_mapping} or {"member"}
    set_roles(tenant.id, user.id, roles)
    return user
```

JIT rules that matter:

- Match users WITHIN the tenant, never across the whole platform. A global email
  match lets tenant A's IdP claim tenant B's user.
- The asserted email domain must match the tenant's verified domain. Without
  this, anyone who controls any IdP can mint sessions for your tenant.
- Decide create-vs-reject: pure JIT auto-creates on first login; SCIM-driven
  tenants should reject unknown users (provisioning is SCIM's job, not the
  assertion's). Make this a per-tenant flag.

## Single Logout (SLO)

SLO is best-effort and frequently flaky across IdPs. Implement it but do not
make session security depend on it.

- SP-initiated: user logs out, you send a signed `<LogoutRequest>` to the IdP's
  SLO endpoint; IdP responds with `<LogoutResponse>`.
- IdP-initiated: IdP POSTs `<LogoutRequest>` to your `/sls`; you verify the
  signature, kill the matching local session, return `<LogoutResponse>`.

Always also expire the local session on a short idle timeout regardless of SLO,
because many IdPs and browsers drop SLO messages silently.

## Common IdP quirks

| IdP | Quirk | Mitigation |
|---|---|---|
| Azure AD / Entra | NameID may be a persistent opaque ID, not email | Map email from `...emailaddress` claim, not NameID |
| Okta | Group attribute only sent if filter configured in the app | Document the group filter in your setup guide |
| ADFS | Sends `http://schemas.xmlsoap.org/.../emailaddress` claim URIs | Allow full-URI attribute names in mapping |
| OneLogin | RelayState handling differs on IdP-initiated | Treat empty RelayState as "go to dashboard" |
| Ping | Strict clock; rejects skew | Run NTP; keep skew tolerance small but nonzero |

## Rotation and operations

- Certificate rotation: IdP signing certs expire. Support TWO valid certs per
  tenant during rollover so login does not break at the cutover instant.
- Metadata refresh: if the tenant supplied a metadata URL, refresh on a schedule
  and alert on signature/cert change (could be rotation, could be compromise).
- Replay cache: store `Assertion.ID` with a TTL equal to the validity window.
  Use a shared store (Redis) so it works across app instances; an in-process
  cache lets replays through on a different node.

## Anti-patterns (do not ship)

- Reading attributes before verifying the signature.
- A single global SP entity ID and ACS shared across tenants.
- Trusting the asserted email without the tenant domain guard.
- In-process replay cache in a multi-instance deployment.
- Making logout (and thus session revocation) depend solely on SLO.
- Disabling signature verification "temporarily" to debug an integration. Debug
  with logging of the parsed-but-rejected reason instead.
