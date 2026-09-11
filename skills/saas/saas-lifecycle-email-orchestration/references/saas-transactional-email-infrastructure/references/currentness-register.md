# Email Infrastructure Currentness Register

Access date: 2026-09-11

Next review: 2026-10-11 for receiver rules; 2027-03-11 for stable RFCs unless superseded earlier.

| Source | Scope | Publication/version | Freshness | Support status | Uncertainty / use |
| --- | --- | --- | --- | --- | --- |
| [RFC 7208](https://www.rfc-editor.org/info/rfc7208/) | SPF | April 2014 | Durable | Standards Track | Verify errata and provider-specific generation; do not copy sample records |
| [RFC 6376](https://www.rfc-editor.org/rfc/rfc6376.html) | DKIM | September 2011 | Durable | Standards Track | Verify errata and current cryptographic/provider constraints |
| [RFC 9989](https://www.rfc-editor.org/info/rfc9989/) | DMARC | 2026 | Current | Proposed Standard; obsoletes RFC 7489 and RFC 9091 | New standard; receiver and tooling implementation coverage may lag |
| [RFC 8058](https://www.rfc-editor.org/info/rfc8058/) | One-click unsubscribe | January 2017 | Durable | Standards Track | Apply only to relevant subscribed/marketing traffic and current receiver rules |
| [Gmail email sender guidelines](https://support.google.com/mail/answer/81126?hl=en) and [FAQ](https://support.google.com/mail/answer/14229414?hl=en) | Gmail personal-account sender requirements | Live; enforcement update noted November 2025 | Highly volatile | Active | Requirements and thresholds are receiver-specific; reopen before release |
| [Yahoo Sender Best Practices](https://senders.yahooinc.com/best-practices/) | Yahoo bulk-sender requirements | Live | Highly volatile | Active | Reopen before release; do not infer requirements for other networks |

## Admission rule

Before adding a threshold, key size, DNS field, unsubscribe behaviour, volume classification,
provider feature, or receiver requirement to a production decision:

1. open the primary source;
2. record the exact recipient network and traffic class;
3. capture publication/update date when available and access date;
4. distinguish requirement from recommendation;
5. record support/tooling evidence and uncertainty;
6. assign an owner and review date;
7. mark unsupported or stale claims `NOT ASSESSED`.

Provider pricing, rankings, default-stack recommendations, and generic inbox-placement targets are
intentionally absent. They require a dated workload-specific evaluation.
