---
name: playwright
description: >
  Write, maintain, and debug Playwright end-to-end tests including page objects,
  locators, assertions, fixtures, configuration, tracing, and visual regression.
  Covers Playwright v1.40+ sync and async APIs, test runner, and Browser Mode.
  USE FOR: e2e tests, page objects, locators, assertions, fixtures, config,
  tracing, screenshots, API testing, auth states, codegen, visual regression.
  DO NOT USE FOR: unit tests (use vitest/jest), component tests (use storybook),
  playwright-test-healer mode (use that for fixing failing tests).
location: .roo/skills/playwright/SKILL.md
metadata:
  created: "2026-04-27"
  version: "1.0.0"
  compatibility:
    - playwright>=1.40
    - @playwright/test>=1.40
---

# Playwright E2E Testing Skill

## When to Use This Skill

- Writing new Playwright end-to-end tests
- Creating Page Object Model classes
- Debugging failing E2E tests
- Configuring playwright.config.ts
- Adding locators and assertions
- Setting up test fixtures and auth states
- Implementing visual regression tests
- Using Playwright API testing (request context)
- Setting up tracing and video capture

## When NOT to Use This Skill

- Unit testing React components → use vitest skill
- Component testing → use storybook skill
- Fixing failing Playwright tests → use playwright-test-healer mode
- Generating tests from specs → use playwright-test-generator mode

## Inputs Required

1. Target application URL/baseURL
2. Pages/components to test
3. Test scenarios (user stories or specs)
4. Existing page objects to extend (if any)

## Workflow

### Step 1: Create Playwright Configuration

Study `/tmp/playwright-repo/examples/todomvc/playwright.config.ts` for patterns:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['list']],
  use: {
    actionTimeout: 0,
    trace: 'on-first-retry',
    video: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: true,
  },
});
```

### Step 2: Create Base Page Object

Pattern from `/tmp/playwright-repo` source and project's `tests/e2e/ui/pages/base_page.py`:

```python
from playwright.sync_api import Page, Locator, expect

class BasePage:
    """Base class for all Page Objects."""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        self.page.goto(url)
    
    def get_by_text(self, text: str) -> Locator:
        return self.page.get_by_text(text)
    
    def get_by_role(self, role: str, name: str | None = None) -> Locator:
        return self.page.get_by_role(role, name=name)
    
    def get_by_label(self, label: str) -> Locator:
        return self.page.get_by_label(label)
    
    def get_by_placeholder(self, placeholder: str) -> Locator:
        return self.page.get_by_placeholder(placeholder)
    
    def get_by_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)
    
    def get_title(self) -> str:
        return self.page.title()
```

### Step 3: Create Specific Page Object

Pattern from project's `tests/e2e/ui/pages/login_page.py`:

```python
import re
from playwright.sync_api import Page, expect
from tests.e2e.ui.pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for the Login Page."""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
    
    def navigate(self):
        login_url = f"{self.base_url.rstrip('/')}/login"
        self.page.goto(login_url)
    
    def verify_loaded(self):
        """Verify that the login page has loaded correctly."""
        expect(self.page).to_have_title("Torro Enterprise UI", timeout=10000)
        expect(self.username_input).to_be_visible(timeout=10000)
        expect(self.password_input).to_be_visible(timeout=10000)
        expect(self.login_button).to_be_visible(timeout=10000)
    
    @property
    def username_input(self):
        return self.page.locator("#login_name, input[name='username']")
    
    @property
    def password_input(self):
        return self.page.locator("#login_password, input[name='password']")
    
    @property
    def login_button(self):
        return self.page.get_by_role("button", name=re.compile(r"(sign\s?in|login)", re.IGNORECASE))
    
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

### Step 4: Write Test Files

Pattern from `/tmp/playwright-repo/examples/github-api/tests/test-api.spec.ts`:

```python
from playwright.sync_api import Page, expect
import pytest

# Test-level configuration using test.use()
test.use({
    "baseURL": "https://api.github.com",
    "extraHTTPHeaders": {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.environ['API_TOKEN']}",
    }
})

# Lifecycle hooks
def test_before_all(request, browser):
    """Setup before all tests."""
    pass

def test_after_all(browser):
    """Cleanup after all tests."""
    pass

def test_basic_flow(page: Page):
    """Basic test with assertions."""
    page.goto("/login")
    expect(page).to_have_title("Login", timeout=10000)
    
    # Locator-based interactions
    username_input = page.get_by_label("Username")
    password_input = page.get_by_label("Password")
    login_button = page.get_by_role("button", name="Sign in")
    
    username_input.fill("admin")
    password_input.fill("password")
    login_button.click()
    
    # Post-login assertions
    expect(page).to_have_url("/dashboard", timeout=10000)

def test_api_request(context):
    """API testing with Playwright's request context."""
    request = context.request
    
    response = request.get("/api/health")
    assert response.ok()
    
    data = response.json()
    expect(data).to_contain_key("status")
```

### Step 5: Advanced Locator Patterns

From Playwright source code (`/tmp/playwright-repo/packages/playwright/src/index.ts`):

```python
# Text-based locators (most readable)
page.get_by_text("Submit")
page.get_by_text(/Submit\s*Order/, exact=True)

# Role-based locators (accessibility-first)
page.get_by_role("button", name="Submit")
page.get_by_role("link", name="Dashboard")
page.get_by_role("textbox", name="Email")
page.get_by_role("checkbox", name="Accept terms")
page.get_by_role("heading", name="Welcome", level=2)

# Label-based locators (form elements)
page.get_by_label("Username")
page.get_by_label("Password")

# Placeholder-based locators
page.get_by_placeholder("Search...")

# Test ID locators (most stable)
page.get_by_test_id("submit-button")

# CSS locators (fallback)
page.locator("button.submit-btn")
page.locator("#form > .field > input[type='text']")

# XPath locators (last resort)
page.locator("//button[contains(text(), 'Submit')]")

# Nested locators
page.locator("form").get_by_role("button", name="Submit")
page.get_by_role("row").filter(has_text="Active").get_by_role("button", name="Edit")
```

### Step 6: Assertions

From Playwright expect library (`/tmp/playwright-repo/packages/playwright/src/matchers/expect.ts`):

```python
from playwright.sync_api import expect

# Element state assertions
expect(locator).to_be_visible()
expect(locator).to_be_hidden()
expect(locator).to_be_enabled()
expect(locator).to_be_disabled()
expect(locator).to_be_checked()
expect(locator).to_be_focused()
expect(locator).to_be_empty()
expect(locator).to_be_attached()

# Content assertions
expect(locator).to_have_text("Expected Text")
expect(locator).to_contain_text("Partial")
expect(locator).to_have_value("input value")
expect(page).to_have_title("Page Title")
expect(page).to_have_url("https://example.com/page")

# Attribute assertions
expect(locator).to_have_attribute("href", "/dashboard")
expect(locator).to_have_attribute("data-testid", "submit-btn")
expect(locator).to_have_class("btn btn-primary")
expect(locator).to_have_id("main-container")
expect(locator).to_have_css("color", "rgb(0, 0, 0)")
expect(locator).to_have_js_property("disabled", False)

# Form assertions
expect(locator).to_be_editable()
expect(locator).to_be_disabled()

# Count assertions
expect(locator).to_have_count(5)

# Screenshot assertions
expect(locator).to_have_screenshot()

# Soft assertions (continue on failure)
expect(locator).to_be_visible(timeout=5000)  # hard assertion
# For soft assertions, use test.expect() with soft parameter
```

### Step 7: API Testing

From `/tmp/playwright-repo/examples/github-api/tests/test-api.spec.ts`:

```python
def test_api_workflow(context):
    """Full API workflow with request context."""
    request = context.request
    
    # GET request
    response = request.get("/api/users")
    assert response.ok()
    users = response.json()
    expect(users).to_be_an_instance_of(list)
    
    # POST request
    response = request.post("/api/users", data={
        "name": "New User",
        "email": "user@example.com"
    })
    assert response.ok()
    user = response.json()
    expect(user).to_contain_key("id")
    
    # PUT request
    response = request.put(f"/api/users/{user['id']}", data={
        "name": "Updated Name"
    })
    assert response.ok()
    
    # DELETE request
    response = request.delete(f"/api/users/{user['id']}")
    assert response.ok()
    
    # Request with headers
    response = request.get("/api/protected", headers={
        "Authorization": f"Bearer {token}"
    })
```

### Step 8: Tracing and Debugging

```python
def test_with_tracing(page, test_info):
    """Test with trace capture for debugging."""
    # Tracing is configured in playwright.config.ts
    # trace: 'on-first-retry' or 'retain-on-failure'
    
    page.goto("/login")
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("password")
    page.get_by_role("button", name="Sign in").click()
    
    # Take screenshot on specific steps
    page.screenshot(path="screenshots/dashboard.png")
    
    # Log for debugging
    print(f"Current URL: {page.url}")
    print(f"Page title: {page.title()}")
```

## Troubleshooting

### Locator Not Found

```python
# Use multiple selectors for robustness
page.locator("#login_name, input[name='username'], input#username")

# Use get_by_role for accessibility-first locators
page.get_by_role("textbox", name="Username")

# Add timeout for async elements
expect(locator).to_be_visible(timeout=10000)
```

### Flaky Tests

```python
# Auto-waiting: Playwright auto-waits before actions
page.click("button")  # auto-waits for enabled, visible, etc.

# Explicit waits when needed
expect(page.get_by_text("Loaded")).to_be_visible()

# Retry configuration in config
retries: process.env.CI ? 2 : 0
```

### Network Interception

```python
# Mock API responses
page.route("**/api/users", route => {
    route.fulfill(json=[{"id": 1, "name": "Mock User"}])
})

# Unroute mocks
page.unroute("**/api/users")
```

## Related Files

- `/tmp/playwright-repo/packages/playwright/src/index.ts`
- `/tmp/playwright-repo/packages/playwright/src/matchers/expect.ts`
- `/tmp/playwright-repo/examples/todomvc/playwright.config.ts`
- `/tmp/playwright-repo/examples/github-api/tests/test-api.spec.ts`
- `tests/e2e/ui/pages/base_page.py`
- `tests/e2e/ui/pages/login_page.py`
