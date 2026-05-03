# API Rules From Practical API Building

Use this reference when an API must be pleasant for frontend, mobile, partner, and internal consumers to use over time.

## Start With An Action Plan

- Before writing endpoints, list what each resource must support in plain business language.
- Talk to real consumers: mobile, frontend, partners, support, and business owners.
- Convert actions into resources and subresources only after the required behavior is clear.
- Not every business action needs a new endpoint; many belong as fields, subresources, or command resources on an existing resource.

## Endpoint Shape

- Use plural collection names consistently.
- Prefer nouns in URLs; let HTTP methods carry common verbs.
- Avoid verb-heavy RPC paths unless the domain operation is explicitly a command resource.
- Use subresources where ownership matters, but avoid deeply nested URLs that are hard to authorize and paginate.
- Consider non-sequential public IDs where scraping or business-volume disclosure is a risk.

## Request And Response Rules

- Prefer JSON as the default request/response format unless a real consumer requirement demands another format.
- Do not mix inconsistent wrappers across endpoints.
- Include metadata for pagination and links where clients need navigation.
- Standardize validation errors so clients can map field errors without screen scraping messages.
- Use realistic seed data and acceptance fixtures so client developers can build against meaningful responses.

## Method Decisions

- Use `GET` for safe reads.
- Use `POST` when the server creates a subordinate resource or the client does not know the final URL.
- Use `PUT` when the client knows the full URL and the operation is idempotent replacement/creation.
- Use `PATCH` for partial updates with documented merge semantics.
- Treat destructive bulk delete endpoints as dangerous and usually avoid exposing them.

## Pagination, Embedding, And Filtering

- Every list endpoint needs explicit pagination, default sort, maximum page size, and filter semantics.
- Embedded/nested data should be consistent and intentionally bounded.
- Do not let clients request unbounded deep object graphs.
- If mobile clients need fewer round trips, design includes/embeds deliberately rather than forcing chatty workflows.

## Versioning

- Versioning is a consumer-support problem, not just a routing trick.
- URI versioning is simple but can create URL migration and copy/paste coupling problems.
- Header/media-type versioning can be cleaner but requires consumer education and cache correctness.
- Keep transformers/serializers versioned with the contract so shared implementation code does not accidentally break old clients.
- Publish migration notes, deprecation windows, and tests for supported versions.

## Documentation And Testing

- API documentation should be generated or maintained from a source-of-truth contract.
- Include examples for happy path, validation errors, auth failures, pagination, filtering, and rate limits.
- Endpoint tests should cover method, auth, validation, status code, envelope, pagination, and representative error cases.
- Use dummy but realistic seed data; never require production data for development or tests.

## Consumer Friendliness Check

- Can a new frontend/mobile developer discover the next link or page without asking the backend team?
- Are error codes stable enough for client behavior?
- Is authorization behavior predictable across list/detail/subresource endpoints?
- Can consumers test locally with meaningful seed data?
- Does the versioning approach match the audience's skill level and support needs?
