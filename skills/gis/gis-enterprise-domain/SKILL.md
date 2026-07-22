---
name: gis-enterprise-domain
description: Use when administering ArcGIS Enterprise or building real-estate-specific GIS features — ArcGIS components, publishing services, security/roles, backup/DR, plus property search, neighbourhood analysis, catchment/isochrones, market heatmaps, and real-estate-SaaS integration.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Enterprise and Domain GIS
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Use when administering ArcGIS Enterprise or building real-estate-specific GIS features — ArcGIS components, publishing services, security/roles, backup/DR, plus property search, neighbourhood analysis, catchment/isochrones, market heatmaps, and real-estate-SaaS integration.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Operability | ArcGIS Enterprise admin runbook | Markdown doc per `skill-composition-standards/references/runbook-template.md` covering portal, Server, and Data Store ops | `docs/gis/arcgis-runbook.md` |
| Data safety | Real-estate domain data model | Markdown doc per `skill-composition-standards/references/entity-model-template.md` covering parcel, ownership, and valuation entities | `docs/gis/real-estate-model.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
<!-- dual-compat-end -->
ArcGIS Enterprise administration for regulated / established GIS environments, plus real-estate-specific GIS patterns that map cleanly to PostGIS + map clients.

**Prerequisites:** Load the `gis-platform-engineering` skill for the spatial backend (its `gis-postgis-backend` reference) and the map client (its `gis-mapping` or `gis-maps-integration` reference), and `multi-tenant-saas-architecture` for tenant isolation.

## When this skill applies

- Operating or integrating with ArcGIS Enterprise (Portal, Server, Data Store, Web Adaptor).
- Publishing authoritative GIS services (map, feature, image, geocoding).
- Designing GIS features for real estate: property search, neighbourhood analysis, catchment, market heatmaps.
- Building a real-estate SaaS that needs spatial features at a high bar.

## When ArcGIS Enterprise is right

```text
Government / regulated sector with ArcGIS mandated               -> ArcGIS Enterprise
Team already trained on ArcGIS Pro                               -> ArcGIS Enterprise
Need authoritative imagery/demographics datasets under licence    -> ArcGIS Online/Enterprise
Small startup, modern stack, cost-sensitive                       -> PostGIS + Mapbox/MapLibre
You need ESRI-specific analytical tools (Network Analyst)        -> ArcGIS Enterprise
```

Most SaaS startups pick the PostGIS + OSS map stack. ArcGIS Enterprise earns its cost in sectors where it's already the standard (government, utilities, defence) or when licenced datasets are critical.

See `references/when-arcgis-enterprise.md`.

## ArcGIS Enterprise components

- **Portal for ArcGIS** — identity, sharing, groups, content catalogue.
- **ArcGIS Server** — publishes services (map, feature, image, geoprocessing, geocoding).
- **Data Store** — relational, tile, and spatiotemporal data backends.
- **Web Adaptor** — IIS/Java web server integration for HTTPS, custom URLs.

Typical base deployment: one of each, highly available variant adds replication for each.

See `references/arcgis-components.md`.

## Publishing services

- **Feature services** — CRUD + query on features, the workhorse for interactive apps.
- **Map services** — pre-rendered tiles for fast display at fixed scales.
- **Image services** — raster data (imagery, DEM).
- **Geocoding services** — address to coordinate.
- **GeoProcessing services** — spatial analysis functions as endpoints.

**Versioning:** branch versioning for concurrent editing without conflicts; default version for most read workloads.

See `references/publishing-services.md`.

## Security + roles

Portal users assigned roles: Viewer, Data Editor, Publisher, Administrator. Groups control sharing.

Server-side Role-Based Access Control on published services. Integrate with enterprise IdP (SAML / OIDC).

Audit logs — enable and ship to the SIEM.

See `references/arcgis-security-roles.md`.

## Backup + DR

```text
1. Portal content — webgisdr utility (export + import).
2. Data Store — automated backups + geo-replicate for HA.
3. Server config — backup the machine's `config-store` directory.
4. Web Adaptor — stateless, reinstall from config.
5. Restore drill quarterly.
```

webgisdr is authoritative for Portal/Server/Data Store coordinated backup.

See `references/arcgis-backup-dr.md`.

## Real estate GIS recipes

### Property search with spatial filters

Filter by district/neighbourhood + within walking distance to transit + inside a school zone:

```sql
WITH search_area AS (
  SELECT ST_Union(geom) AS geom FROM districts WHERE code IN ('KAM01', 'KAM02')
), school_zones AS (
  SELECT ST_Union(geom) AS geom FROM zones WHERE type = 'school' AND rating >= 4
), transit AS (
  SELECT ST_Buffer(geom::geography, 800)::geometry AS geom FROM transit_stops  -- 800m walking
)
SELECT l.*
FROM listings l
JOIN search_area s ON ST_Contains(s.geom, l.geom)
JOIN school_zones sz ON ST_Contains(sz.geom, l.geom)
JOIN LATERAL (SELECT 1 FROM transit t WHERE ST_Intersects(t.geom, l.geom) LIMIT 1) tr ON TRUE
WHERE l.tenant_id = :tenant_id AND l.status = 'active';
```

See `references/property-search-spatial.md`.

### Neighbourhood analysis

For a listing, compute:

- **Walk score** — count of amenities within 800m / 1600m weighted by category.
- **Transit access** — nearest N transit stops with travel time.
- **Comparables** — similar listings within 2 km in last 180 days.
- **Demographics** — join to census or tenant-provided block statistics.

Cache per-listing summaries; refresh nightly.

See `references/neighbourhood-analysis.md`.

### Catchment / drive-time isochrones

- Simple: buffer by straight-line distance.
- Better: drive-time isochrones from OSRM, Mapbox Isochrone API, or Google Distance Matrix.
- Cache isochrone polygons in PostGIS; key by (point, mode, minutes).
- Use in "find listings I can reach in 20 minutes" features.

```sql
CREATE TABLE isochrones (
  id serial PRIMARY KEY,
  point geometry(Point, 4326) NOT NULL,
  mode text NOT NULL,
  minutes int NOT NULL,
  geom geometry(Polygon, 4326) NOT NULL,
  computed_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (point, mode, minutes)
);
```

See `references/catchment-isochrones.md`.

### Market heatmaps

Heatmap of listing price per square metre by small area (H3 hex index, grid, or admin boundary):

```sql
SELECT h.cell, AVG(l.price_per_sqm) AS avg_price, COUNT(*) AS listings
FROM listings l
JOIN h3_cells_resolution_8 h ON h3_indexes_contain(h.cell, l.geom)
WHERE l.tenant_id = :tenant_id AND l.sold_date > now() - interval '180 days'
GROUP BY h.cell
HAVING COUNT(*) >= 5;
```

Render client-side as a choropleth on Mapbox/MapLibre. Suppress cells with low N to avoid privacy + noise.

See `references/market-heatmaps.md`.

### Real-estate-SaaS integration

Architecture:

```text
Web app (Next.js/React)
  -> API (Fastify/PHP) reads MySQL listings table
  -> API joins to PostGIS for spatial queries
  -> Client renders map (Mapbox GL with MVT tiles from PostGIS)
  -> Geocoding via Google Places (cached)
  -> Isochrones via Mapbox Isochrone (cached in PostGIS)
```

Keep transactional listing data in MySQL; keep spatial in PostGIS; keep them linked by `listing_id`.

See `references/real-estate-saas-integration.md`.

## Anti-patterns

- Double-entry of property location in MySQL and PostGIS without a canonical source.
- Heatmaps rendered per-request without caching (expensive queries every pan/zoom).
- Isochrones computed live instead of cached.
- Exposing raw ArcGIS service URLs on the public internet without auth and rate limits.
- ArcGIS Enterprise on a single node for production (no HA).
- No webgisdr backup schedule.
- Publishing feature services without field-level visibility rules for multi-tenant contexts.

## Read next

## Decision rules

| Condition | Choice | Failure avoided |
|---|---|---|
| Governed internal services need ArcGIS tooling | Use ArcGIS Enterprise with explicit HA and backup design | Unsupported single-node production |
| Public workload is an application-specific spatial API | Prefer PostGIS platform engineering | Excess licensing and operational coupling |
| Analysis is expensive but inputs change slowly | Precompute and cache by versioned inputs | Repeated isochrone or heatmap cost |

## Capability contract

Read and search the service inventory, topology rules, roles, and recovery requirements first. Administrative changes require explicit authorisation; execute non-destructive checks only in an approved environment.

## Degraded mode

If the ArcGIS environment or service metadata is unavailable, provide a read-only assessment and mark publishing, topology, security, capacity, and recovery conclusions as unverified.

- `gis-platform-engineering` skill (its `gis-postgis-backend` reference) — spatial backbone.
- `gis-platform-engineering` skill (its `gis-maps-integration` reference) — client mapping.
- `multi-tenant-saas-architecture` — tenant isolation end-to-end.

## References

- `references/when-arcgis-enterprise.md`
- `references/arcgis-components.md`
- `references/publishing-services.md`
- `references/arcgis-security-roles.md`
- `references/arcgis-backup-dr.md`
- `references/property-search-spatial.md`
- `references/neighbourhood-analysis.md`
- `references/catchment-isochrones.md`
- `references/market-heatmaps.md`
- `references/real-estate-saas-integration.md`
- `references/arcgis-pro-workflows.md` — geodatabase invariants, topology rules for parcels, branch vs traditional versioning, georeferencing with RMS targets, service pre-flight checklist
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| Domain entities, spatial operations, coordinate systems, accuracy, and governance requirements | yes | Model enterprise GIS behaviour |
## Outputs
- Produce GIS domain model, spatial rules, data quality controls, and operational evidence.
