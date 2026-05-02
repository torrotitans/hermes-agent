---
name: msw
description: >
  Create and maintain MSW (Mock Service Worker) mocks for API testing, development,
  and E2E testing. Covers http handlers, graphql handlers, HttpResponse, request
  matching, resolver functions, browser worker deployment, and test setup.
  USE FOR: API mocking, handler creation, request interception, response mocking,
  development mocks, E2E test mocks, graphql mocking, request parsing.
  DO NOT USE FOR: Playwright tests (use playwright skill), Vitest mocking (use vi.fn()),
  backend implementation, real API development.
location: .roo/skills/msw/SKILL.md
metadata:
  created: "2026-04-27"
  version: "1.0.0"
  compatibility:
    - msw>=2.0.0
    - typescript>=5.0
---

# MSW (Mock Service Worker) Skill

## When to Use This Skill

- Creating API mocks for frontend development
- Setting up MSW handlers for E2E testing
- Mocking REST API responses
- Mocking GraphQL API responses
- Creating request interceptors for testing
- Setting up service worker for browser mocking
- Testing error scenarios and edge cases

## When NOT to Use This Skill

- Unit testing with Vitest → use vi.fn() / vi.mock()
- Backend API implementation
- Production API mocking (use real backend)
- Playwright E2E tests without mocking (use playwright skill)

## Inputs Required

1. API endpoints to mock
2. Request/response schemas
3. Test scenarios or development needs
4. Base URL configuration

## Workflow

### Step 1: Install MSW

```bash
# Install MSW as dev dependency
npm install msw --save-dev

# Initialize service worker (creates src/mocks/browser.ts)
npx msw init public/ --save
```

### Step 2: Create MSW Worker Setup

Create `src/mocks/browser.ts`:

```typescript
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

// Create a browser worker instance
export const worker = setupWorker(...handlers);

// Start the worker in development
export async function startWorker() {
  await worker.start({
    onUnhandledRequest: 'bypass', // or 'warn', 'error'
    serviceWorker: {
      url: '/mockServiceWorker.js',
    },
  });
}
```

### Step 3: Create Handler Files

Pattern from [`UI/src/mocks/handlers.ts`](UI/src/mocks/handlers.ts):

```typescript
/**
 * FN:handlers.ts MSW request handlers for all API endpoints
 * 
 * Mocks all backend responses for offline testing
 * Pattern: Match request → return sample data → validate with adapter
 */

import { http, HttpResponse } from 'msw';

const BASE_URL = 'http://localhost:3128';

// ============================================================================
// SAMPLE DATA FIXTURES
// ============================================================================

const sampleConnectors = [
  {
    id: 'conn-s3-prod',
    name: 'Prod S3 Bucket',
    type: 's3',
    status: 'active',
    created_at: '2024-03-01T10:00:00Z',
    discovery_count: 12,
    config: { bucket: 'torro-prod', region: 'us-west-2' },
  },
  {
    id: 'conn-postgres-main',
    name: 'PostgreSQL Prod',
    type: 'postgres',
    status: 'active',
    created_at: '2024-02-15T14:30:00Z',
    discovery_count: 8,
    config: { host: 'db.prod.internal', port: 5432 },
  },
];

const sampleAssets = [
  {
    id: 'asset-orders-001',
    name: 'orders',
    type: 'table',
    connector_id: 'conn-postgres-main',
    status: 'discovered',
    discovered_at: '2024-03-28T08:00:00Z',
    row_count: 1250000,
    size_bytes: 524288000,
    tags: ['finance', 'production'],
  },
  {
    id: 'asset-customers-001',
    name: 'customers',
    type: 'table',
    connector_id: 'conn-postgres-main',
    status: 'approved',
    discovered_at: '2024-03-25T12:00:00Z',
    row_count: 450000,
    size_bytes: 209715200,
    tags: ['crm', 'production'],
  },
];

// ============================================================================
// CONNECTION ENDPOINTS
// ============================================================================

/**
 * FN:GET_connectors List all connections with pagination
 */
http.get(`${BASE_URL}/connectors`, ({ request }) => {
  const url = new URL(request.url);
  const skip = parseInt(url.searchParams.get('skip') || '0', 10);
  const limit = parseInt(url.searchParams.get('limit') || '25', 10);

  const items = sampleConnectors.slice(skip, skip + limit);
  return HttpResponse.json(
    {
      data: items,
      meta: { skip, limit, total: sampleConnectors.length },
    },
    { status: 200 }
  );
});

/**
 * FN:POST_connectors Create new connection
 */
http.post(`${BASE_URL}/connectors`, async ({ request }) => {
  const body = (await request.json()) as any;

  const newConnector = {
    id: `conn-${Date.now()}`,
    name: body.name,
    type: body.type?.toLowerCase(),
    status: 'active',
    created_at: new Date().toISOString(),
    discovery_count: 0,
    config: body.config,
  };

  return HttpResponse.json({ data: newConnector }, { status: 201 });
});

/**
 * FN:GET_connector_detail Get single connection
 */
http.get(`${BASE_URL}/connectors/:id`, ({ params }) => {
  const connector = sampleConnectors.find((c) => c.id === params.id);
  if (!connector) {
    return HttpResponse.json(
      { error: 'Connector not found' },
      { status: 404 }
    );
  }
  return HttpResponse.json({ data: connector }, { status: 200 });
});

/**
 * FN:PUT_connector Update connection
 */
http.put(`${BASE_URL}/connectors/:id`, async ({ params, request }) => {
  const body = (await request.json()) as any;
  const connector = sampleConnectors.find((c) => c.id === params.id);

  if (!connector) {
    return HttpResponse.json(
      { error: 'Connector not found' },
      { status: 404 }
    );
  }

  const updated = { ...connector, ...body };
  return HttpResponse.json({ data: updated }, { status: 200 });
});

/**
 * FN:DELETE_connector Delete connection
 */
http.delete(`${BASE_URL}/connectors/:id`, ({ params }) => {
  const connector = sampleConnectors.find((c) => c.id === params.id);
  if (!connector) {
    return HttpResponse.json(
      { error: 'Connector not found' },
      { status: 404 }
    );
  }
  return HttpResponse.json({ data: { id: params.id } }, { status: 200 });
});

// ============================================================================
// DISCOVERY ENDPOINTS
// ============================================================================

/**
 * FN:POST_discover Trigger discovery job
 */
http.post(`${BASE_URL}/discover`, async ({ request }) => {
  const body = (await request.json()) as any;

  const newJob = {
    id: `job-disc-${Date.now()}`,
    connector_id: body.connector_id,
    job_id: `airflow_task_${Date.now()}`,
    status: 'in_progress',
    started_at: new Date().toISOString(),
    assets_found: 0,
    progress: 0,
  };

  return HttpResponse.json({ data: newJob }, { status: 202 });
});

/**
 * FN:GET_discovery_poll Poll discovery job status
 */
http.get(`${BASE_URL}/discover/:id/poll`, ({ params }) => {
  const job = sampleJobs.find((j) => j.id === params.id);
  if (!job) {
    return HttpResponse.json(
      { error: 'Job not found' },
      { status: 404 }
    );
  }
  return HttpResponse.json({ data: job }, { status: 200 });
});

// ============================================================================
// ASSET ENDPOINTS
// ============================================================================

/**
 * FN:GET_assets List all assets with filtering
 */
http.get(`${BASE_URL}/assets`, ({ request }) => {
  const url = new URL(request.url);
  const skip = parseInt(url.searchParams.get('skip') || '0', 10);
  const limit = parseInt(url.searchParams.get('limit') || '25', 10);
  const status = url.searchParams.get('status');

  let items = sampleAssets;
  if (status) {
    items = items.filter((a) => a.status === status);
  }

  const paginated = items.slice(skip, skip + limit);
  return HttpResponse.json(
    {
      data: paginated,
      meta: { skip, limit, total: items.length },
    },
    { status: 200 }
  );
});

/**
 * FN:GET_asset_detail Get single asset
 */
http.get(`${BASE_URL}/assets/:id`, ({ params }) => {
  const asset = sampleAssets.find((a) => a.id === params.id);
  if (!asset) {
    return HttpResponse.json(
      { error: 'Asset not found' },
      { status: 404 }
    );
  }
  return HttpResponse.json({ data: asset }, { status: 200 });
});

/**
 * FN:PUT_asset_approval Update asset approval status
 */
http.put(`${BASE_URL}/assets/:id/approval`, async ({ params, request }) => {
  const body = (await request.json()) as any;
  const asset = sampleAssets.find((a) => a.id === params.id);

  if (!asset) {
    return HttpResponse.json(
      { error: 'Asset not found' },
      { status: 404 }
    );
  }

  const updated = { ...asset, ...body };
  return HttpResponse.json({ data: updated }, { status: 200 });
});

// ============================================================================
// LINEAGE ENDPOINTS
// ============================================================================

/**
 * FN:POST_lineage_neighbors Get lineage neighbors
 */
http.post(`${BASE_URL}/lineage/neighbors`, async ({ request }) => {
  const body = (await request.json()) as any;
  // Return sample lineage data
  return HttpResponse.json(
    {
      nodes: [
        { id: 'asset-customers-001', name: 'customers', type: 'table' },
        { id: 'report-analysis', name: 'analysis', type: 'view' },
      ],
      edges: [
        {
          source: 'asset-customers-001',
          target: 'report-analysis',
          relationship: 'feeds',
        },
      ],
    },
    { status: 200 }
  );
});

/**
 * FN:GET_health Health check endpoint
 */
http.get(`${BASE_URL}/health`, () => {
  return HttpResponse.json(
    {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
    },
    { status: 200 }
  );
});
```

### Step 4: Handler Patterns from MSW Source

From [`/tmp/msw-repo/src/core/http.ts`](/tmp/msw-repo/src/core/http.ts):

```typescript
import { http, HttpResponse } from 'msw';

// HTTP method shortcuts
http.get(url, resolver)
http.post(url, resolver)
http.put(url, resolver)
http.patch(url, resolver)
http.delete(url, resolver)
http.head(url, resolver)
http.all(url, resolver) // Match any method

// Path parameters
http.get('/users/:id', ({ params }) => {
  return HttpResponse.json({ id: params.id, name: 'John' });
});

// Query string parsing
http.get('/users', ({ request }) => {
  const url = new URL(request.url);
  const page = url.searchParams.get('page');
  const limit = url.searchParams.get('limit');
  // ...
});

// Regex path matching
http.get(/\/api\/users\/\d+/, ({ params }) => {
  return HttpResponse.json({ id: params[0] });
});
```

### Step 5: HttpResponse API

From [`/tmp/msw-repo/src/core/HttpResponse.ts`](/tmp/msw-repo/src/core/HttpResponse.ts):

```typescript
import { http, HttpResponse } from 'msw';

// JSON response (most common)
http.get('/users', () => {
  return HttpResponse.json({ id: 1, name: 'John' });
});

// Text response
http.get('/health', () => {
  return HttpResponse.text('OK');
});

// Custom headers
http.get('/users', () => {
  return HttpResponse.json(
    { id: 1, name: 'John' },
    {
      status: 200,
      headers: {
        'X-Custom-Header': 'value',
        'Cache-Control': 'no-cache',
      },
    }
  );
});

// Error responses
http.get('/users/:id', ({ params }) => {
  if (!params.id) {
    return HttpResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }
  return HttpResponse.json({ id: params.id, name: 'John' });
});

// Redirect responses
http.get('/old-path', () => {
  return HttpResponse.redirect('/new-path');
});

// Error responses (special)
http.get('/users', () => {
  return HttpResponse.error();
});

// Async resolvers
http.post('/users', async ({ request }) => {
  const body = await request.json();
  // Simulate async operation
  await new Promise(resolve => setTimeout(resolve, 100));
  return HttpResponse.json({ id: Date.now(), ...body });
});
```

### Step 6: Request Parsing

```typescript
import { http, HttpResponse } from 'msw';

// Parse JSON body
http.post('/users', async ({ request }) => {
  const body = await request.json();
  return HttpResponse.json({ created: true, ...body });
});

// Parse form data
http.post('/upload', async ({ request }) => {
  const formData = await request.formData();
  const file = formData.get('file');
  return HttpResponse.json({ uploaded: true });
});

// Parse URL search params
http.get('/search', ({ request }) => {
  const url = new URL(request.url);
  const q = url.searchParams.get('q');
  const page = url.searchParams.get('page');
  return HttpResponse.json({ results: [], query: q, page });
});

// Access request headers
http.get('/users', ({ request }) => {
  const auth = request.headers.get('Authorization');
  // ...
});

// Access request cookies
http.get('/users', ({ cookies }) => {
  const token = cookies.session;
  // ...
});
```

### Step 7: Conditional and Delayed Responses

```typescript
import { http, HttpResponse } from 'msw';

// Simulate network delay
http.get('/users', () => {
  return new HttpResponse(null, {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
});

// Conditional responses based on headers
http.get('/users', ({ request }) => {
  const format = request.headers.get('Accept');
  if (format === 'application/xml') {
    return HttpResponse.xml('<users></users>');
  }
  return HttpResponse.json({ users: [] });
});

// Simulate errors
http.get('/users', ({ request }) => {
  if (request.headers.get('Authorization')?.includes('invalid')) {
    return HttpResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }
  return HttpResponse.json({ users: [] });
});

// Delayed response
http.get('/slow-endpoint', () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(HttpResponse.json({ data: 'slow' }));
    }, 2000);
  });
});
```

### Step 8: MSW for Node (Testing)

```typescript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Step 9: GraphQL Handlers

```typescript
import { graphql } from 'msw';

graphql.query('GetUser', ({ variables }) => {
  return HttpResponse.json({
    data: {
      user: { id: variables.id, name: 'John' },
    },
  });
});

graphql.mutation('CreateUser', async ({ variables }) => {
  const body = await variables;
  return HttpResponse.json({
    data: {
      createUser: { id: Date.now(), ...body },
    },
  });
});

graphql.query('GetUsers', ({ request }) => {
  // Access query string
  const url = new URL(request.url);
  const limit = url.searchParams.get('limit');
  return HttpResponse.json({
    data: { users: [] },
  });
});
```

## Troubleshooting

### Service Worker Not Intercepting

```typescript
// Ensure worker is started before tests
await worker.start({
  onUnhandledRequest: 'bypass',
});

// Check that public/mockServiceWorker.js exists
// Verify service worker is registered in browser DevTools
```

### Handler Not Matching

```typescript
// Check BASE_URL matches request URL
const BASE_URL = 'http://localhost:3128';

// Use exact path matching
http.get(`${BASE_URL}/users`, ...);

// For wildcard matching, use regex
http.get(/\/api\/.*/, ...);
```

### TypeScript Type Errors

```typescript
// Use typed params
interface UserParams {
  id: string;
}

http.get<{ id: string }>('/users/:id', ({ params }) => {
  // params.id is typed as string
});
```

## Related Files

- [`/tmp/msw-repo/src/core/http.ts`](/tmp/msw-repo/src/core/http.ts)
- [`/tmp/msw-repo/src/core/HttpResponse.ts`](/tmp/msw-repo/src/core/HttpResponse.ts)
- [`/tmp/msw-repo/src/core/handlers/HttpHandler.ts`](/tmp/msw-repo/src/core/handlers/HttpHandler.ts)
- [`/tmp/msw-repo/src/core/handlers/RequestHandler.ts`](/tmp/msw-repo/src/core/handlers/RequestHandler.ts)
- [`UI/src/mocks/handlers.ts`](UI/src/mocks/handlers.ts)
