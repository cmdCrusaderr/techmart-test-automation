import pytest
from playwright.sync_api import expect

BASE_URL = "http://localhost:3000"


@pytest.fixture(autouse=True)
def reset_cart(page):
    page.request.delete(f"{BASE_URL}/api/cart")
    yield


def test_add_item_to_cart(page):
    page.goto(BASE_URL)
    page.locator(".add-to-cart-btn").first.click()
    expect(page.locator("#toast")).to_be_visible()
    expect(page.locator("#cartCount")).to_have_text("1")


def test_cart_page_shows_added_item(page):
    page.goto(BASE_URL)
    page.locator(".add-to-cart-btn").first.click()
    page.locator(".cart-link").click()
    expect(page.locator(".cart-item")).to_have_count(1)


def test_update_item_quantity(page):
    page.goto(BASE_URL)
    page.locator(".add-to-cart-btn").first.click()
    page.locator(".cart-link").click()
    expect(page.locator(".qty-value")).to_have_text("1")
    page.locator(".qty-btn", has_text="+").click()
    expect(page.locator(".qty-value")).to_have_text("2")


def test_remove_item_from_cart(page):
    page.goto(BASE_URL)
    page.locator(".add-to-cart-btn").first.click()
    page.locator(".cart-link").click()
    page.locator(".remove-btn").click()
    expect(page.locator("#emptyCart")).to_be_visible()


def test_clear_entire_cart(page):
    page.goto(BASE_URL)
    page.locator(".add-to-cart-btn").nth(0).click()
    page.locator(".add-to-cart-btn").nth(1).click()
    page.locator(".cart-link").click()
    page.locator("#clearCartBtn").click()
    expect(page.locator("#emptyCart")).to_be_visible()


def test_empty_cart_shows_message(page):
    page.goto(f"{BASE_URL}/cart.html")
    expect(page.locator("#emptyCart")).to_be_visible()
