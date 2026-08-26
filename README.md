# TechMart Test Automation Suite

A Python test automation suite covering an e-commerce web app (TechMart) end to end: UI flows via Playwright, edge cases, and network-level mocking, plus a CI pipeline that runs the whole thing on every push.

## What's being tested

The system under test is **TechMart Demo Store**, a small Node/Express e-commerce app (product catalog, cart, auth, checkout) purpose-built as a testing target, from [beaucarnes/software-testing-course](https://github.com/beaucarnes/software-testing-course). It lives in `sample-app/` here, untouched — this repo is the test suite, not the app.

## Test suite

| File | Covers |
|---|---|
| `tests/test_homepage.py` | Page load, title, welcome heading, product count |
| `tests/test_auth.py` | Login (valid/invalid), registration, password mismatch, logout |
| `tests/test_cart.py` | Add/update/remove items, clear cart, empty-cart state |
| `tests/test_checkout.py` | Form display, order summary, input formatting, full checkout flow, field validation |
| `tests/test_edge_cases.py` | Malformed/special-character search input, duplicate cart adds, duplicate email registration, direct URL navigation, cart persistence |
| `tests/test_mocking.py` | Simulated server errors, slow responses, out-of-stock states, and network timeouts via request interception |

34 tests total, run with `pytest`, using Playwright's Python bindings to drive a real Chromium browser.

## Running it

Start the app:
```bash
cd sample-app
npm install
npm start
```

In a separate terminal, run the tests:
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest -v
```

## CI

`.github/workflows/test.yml` starts the Node app and runs the full Python test suite on every push, uploading the results as a build artifact.

## AI-native testing (KaneAI)

Alongside the scripted Playwright suite above, one scenario was also run through [KaneAI](https://www.lambdatest.com/kane-ai) (LambdaTest's AI-native test authoring tool) as a comparison point: instead of writing locators and assertions by hand, you describe the test in plain English and an AI agent figures out the concrete actions at runtime.

The local TechMart instance was exposed to KaneAI's cloud runner via a [cloudflared](https://github.com/cloudflare/cloudflared) tunnel (`cloudflared tunnel --url http://localhost:3000`).

**TC-2 — Verify TechMart Homepage Content** (a 3-step natural-language scenario, expanded by the AI into 7 concrete sub-actions):

1. Go to the homepage → check "Welcome to TechMart" heading is visible → assert true
2. Get the page title → assert it contains "TechMart"
3. Check "Welcome to TechMart" text is visible → assert true

Result: **7/7 steps passed.**

This covers the same ground as `test_homepage_loads` and `test_welcome_heading_visible` in `tests/test_homepage.py`, which makes for a direct comparison: the scripted version is explicit and fully version-controlled — you can read exactly what it checks and why it failed — while the AI-authored version is faster to write and more resilient to small markup changes, at the cost of precision about what it's actually doing under the hood.

## What this demonstrates (and what it honestly doesn't)

This project targets the core, learnable skills of a test-automation role: Python test automation, functional/regression/edge-case testing, CI/CD, and exposure to both traditional scripted and AI-native testing approaches. 