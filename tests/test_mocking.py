import json
import re
import time
from playwright.sync_api import expect

BASE_URL = "http://localhost:3000"


def test_error_state_when_api_fails(page):
    def handle_route(route):
        route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "Internal server error"}),
        )

    page.route("**/api/products*", handle_route)
    page.goto(BASE_URL)
    expect(page.locator(".product-card")).to_have_count(0)


def test_slow_api_response_handled_gracefully(page):
    def handle_route(route):
        time.sleep(3)
        route.continue_()

    page.route("**/api/products*", handle_route)
    page.goto(BASE_URL)
    expect(page.locator(".logo")).to_be_visible()
    expect(page.locator("#searchInput")).to_be_visible()
    expect(page.locator(".product-card")).to_have_count(6, timeout=10000)


def test_out_of_stock_displayed_correctly(page):
    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {"id": 1, "name": "Wireless Headphones", "price": 79.99,
                 "category": "electronics", "image": "headphones.svg", "stock": 0},
                {"id": 2, "name": "Mechanical Keyboard", "price": 129.99,
                 "category": "electronics", "image": "keyboard.svg", "stock": 8},
            ]),
        )

    page.route("**/api/products*", handle_route)
    page.goto(BASE_URL)
    product_cards = page.locator(".product-card")
    expect(product_cards).to_have_count(2)
    # Find by name instead of .first: the frontend sorts products (default
    # "Name" sort), so DOM order doesn't match our mocked array order.
    out_of_stock_card = page.locator(".product-card", has_text="Wireless Headphones")
    expect(out_of_stock_card.locator(".product-stock")).to_contain_text(
        re.compile("out of stock|0", re.IGNORECASE)
    )


def test_add_to_cart_failure_shows_feedback(page):
    page.goto(BASE_URL)

    def handle_cart_route(route):
        if route.request.method == "POST":
            route.fulfill(
                status=400,
                content_type="application/json",
                body=json.dumps({"error": "Insufficient stock"}),
            )
        else:
            route.continue_()

    page.route("**/api/cart", handle_cart_route)
    page.locator(".add-to-cart-btn").first.click()
    expect(page.locator("#toast")).to_be_visible()


def test_network_timeout_handled(page):
    def handle_route(route):
        route.abort("timedout")

    page.route("**/api/products*", handle_route)
    page.goto(BASE_URL)
    expect(page.locator(".logo")).to_be_visible()
    expect(page.locator(".product-card")).to_have_count(0)
