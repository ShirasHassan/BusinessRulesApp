# nTouchAxon — API Integration Portal: Agent Brief

Read this file and `brand/brand.json` only. Everything else is yours to design.

## 0. Preconditions (stop if unmet)
- `brand/brand.json` exists and `source` is `https://nasneuron.com/`. If not: run `cd brand && npm i -D playwright && node extract-brand.mjs`.
- Use `brand/assets/logo-*` (choose the header logo on a light background; the footer logo is the fallback for dark backgrounds). Never redraw or recolor the logo.

## 1. Goal
A developer portal named **nTouchAxon** from **NAS Neuron Health Services** (UAE health-insurance TPA). Partners (insurers, brokers, providers, HR systems) use it to find and try the APIs that push data into and read data from the NAS Neuron system.

## 2. Stack (fixed; don't debate it)
Vite + React + TypeScript + Tailwind. React Router. Put the API reference in OpenAPI 3.1 YAML under `public/specs/` and render it with `@scalar/api-reference-react`. No backend; the "try it" calls go to a sandbox URL set through the env var `VITE_SANDBOX_BASE_URL`.
Location: `ntouchaxon/portal/`.

## 3. Theme mapping (brand.json → tailwind.config `theme.extend.colors`)
| Token | Source in brand.json |
|---|---|
| `primary` | `cssVars` brand var if present, else `elements.header.bg`, else the first non-white/black in `paletteHex` |
| `accent` | `elements.button.bg` |
| `ink` | `elements.body.color` |
| `surface` | white / `elements.body.bg` |
| `footer` | `elements.footer.bg` |
| font | `elements.body.font`, loaded from `fontLinks` |
Put the tokens in `src/theme.ts` as the single source of truth. Text on the primary and accent colors must meet WCAG AA contrast.

## 4. Pages
1. `/` **Landing**
   - Header: logo, nTouchAxon wordmark, nav (APIs, Docs, Sandbox, Support), a "Get API Key" button.
   - Hero: "Connect to NAS Neuron in hours, not months." Subtext: secure REST APIs for policy and claims integration. Two CTAs: Explore APIs, Read Quickstart.
   - Two product cards, each listing a direction and a sample of its endpoints:
     - **Policy Integration APIs**: *Push* (create/renew/endorse policies, add/delete members) · *Read* (policy, members, benefits, eligibility).
     - **Claims Integration APIs**: *Push* (submit settled claims, bulk batch upload) · *Pull* (claims by status/date, claim detail, remittance, webhooks).
   - "How it works" in 3 steps: Register → Get sandbox keys → Go live.
   - Trust strip: OAuth 2.0, TLS 1.2+, audit logs, UAE data residency (label this *placeholder: confirm*).
   - Footer with contact details from brand.json/source site.
2. `/apis/policy` and `/apis/claims`: an overview plus the Scalar reference for the spec.
3. `/docs/quickstart`: auth (OAuth2 client-credentials), environments, idempotency, pagination, errors, webhooks.
4. `/support`: a contact form (UI only) and an FAQ.

## 5. Endpoint catalog (write it as OpenAPI; illustrative, marked `x-status: draft`)
Base: `/v1`. Auth: bearer (OAuth2 client credentials). Write calls require an `Idempotency-Key` header. Lists use cursor pagination (`?cursor=&limit=`). Errors use RFC 7807.
**policy.yaml**
- `POST /policies` create · `PUT /policies/{policyNo}` renew/endorse · `GET /policies/{policyNo}` · `GET /policies?updatedSince=`
- `POST /policies/{policyNo}/members` add (bulk array) · `DELETE /policies/{policyNo}/members/{memberId}` · `GET /policies/{policyNo}/members`
- `GET /members/{memberId}/benefits` · `GET /members/{memberId}/eligibility?date=`
**claims.yaml**
- `POST /claims/settled` push one settled claim · `POST /claims/batches` bulk upload (async, returns `batchId`) · `GET /claims/batches/{batchId}` status
- `GET /claims?status=&from=&to=&policyNo=` pull · `GET /claims/{claimId}` · `GET /claims/{claimId}/remittance`
- `POST /webhooks` subscribe (`claim.settled`, `claim.rejected`, `policy.updated`)
Minimum schemas: Policy, Member, Benefit, Claim (id, memberId, providerId, serviceDate, diagnosis[ICD-10], lines[], amounts{claimed, approved, paid}, currency AED, status), Batch, Problem.

## 6. Acceptance criteria
- `npm run build` and `npm run lint` pass. Lighthouse scores ≥ 90 for accessibility and performance on `/`.
- Layout works at 360px and 1440px widths. Supports dark mode through the tokens.
- No hard-coded hex values outside `theme.ts`.
- Both specs validate (`npx @redocly/cli lint public/specs/*.yaml`).
- Put a screenshot of `/` next to `brand/assets/reference-home.png` in the PR so the design can be compared visually.

## 7. Out of scope
Real auth/API-key issuance, a backend, analytics, CMS.
