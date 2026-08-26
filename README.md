# TechMart Test Automation Suite

A Python test automation suite covering an e-commerce web app (TechMart) end to end: UI flows via Playwright, edge cases, and network-level mocking, plus a CI pipeline that runs the whole thing on every push.

Built while preparing for a Software Test Automation Engineer role, with the test coverage shaped around what that kind of role actually asks for: functional testing, regression/edge-case testing, and CI/CD integration.

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

## What this demonstrates (and what it honestly doesn't)

This project targets the core, learnable skills of a test-automation role: Python test automation, functional/regression/edge-case testing, and CI/CD. It does not attempt to simulate real optical/networking lab hardware (IXIA traffic generators, SCPI/NI-VISA instrument control, Layer 1/2 protocol testing) — those require physical equipment this project doesn't have access to, and faking them wouldn't be an honest representation of hands-on experience.
