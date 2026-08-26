import re
import pytest
from playwright.sync_api import expect

BASE_URL = "http://localhost:3000"


@pytest.fixture(autouse=True)
def reset_and_visit_home(page):
    page.request.delete(f"{BASE_URL}/api/cart")
    page.goto(BASE_URL)
    yield


def test_empty_search_shows_all_products(page):
    page.locator("#searchBtn").click()
    page.wait_for_timeout(500)
    expect(page.locator(".product-card")).to_have_count(6)


def test_nonsense_search_shows_no_results(page):
    page.locator("#searchInput").fill("xyznonexistent123")
    page.locator("#searchBtn").click()
    page.wait_for_timeout(500)
    expect(page.locator(".product-card")).to_have_count(0)


def test_special_characters_in_search_dont_break_page(page):
    page.locator("#searchInput").fill('<script>alert("xss")</script>')
    page.locator("#searchBtn").click()
    page.wait_for_timeout(500)
    expect(page.locator(".product-card")).to_have_count(0)
    expect(page.locator(".logo")).to_be_visible()


def test_whitespace_only_search_returns_no_results(page):
    # The app does not trim whitespace before matching, so "   " is treated
    # as a real (non-empty) search term and matches nothing. Confirmed against
    # the live API (GET /api/products?search=%20%20%20 -> []), not a frontend
    # bug. Worth flagging as a minor UX inconsistency in a real bug report,
    # but this documents the app's actual current behavior.
    page.locator("#searchInput").fill("   ")
    page.locator("#searchBtn").click()
    page.wait_for_timeout(500)
    expect(page.locator(".product-card")).to_have_count(0)


def test_adding_same_product_multiple_times_increments_count(page):
    add_button = page.locator(".add-to-cart-btn").first
    add_button.click()
    page.wait_for_timeout(300)
    add_button.click()
    page.wait_for_timeout(300)
    add_button.click()
    page.wait_for_timeout(500)
    expect(page.locator("#cartCount").first).to_have_text("3")


# Note: no "checkout blocked with empty cart via toast" test here. The app
# redirects straight to /cart.html before the checkout form even renders
# when the cart is empty (confirmed by test_redirects_to_cart_if_empty in
# test_checkout.py), so the form-fill-then-toast scenario from the reference
# suite isn't actually reachable — the earlier redirect already covers this
# behavior more directly.


def test_registration_requires_all_fields(page):
    page.goto(f"{BASE_URL}/register.html")
    page.locator("#email").fill("test@example.com")
    page.locator('button[type="submit"]').click()
    expect(page).to_have_url(re.compile("register"))


def test_duplicate_email_registration_rejected(page):
    page.goto(f"{BASE_URL}/register.html")
    page.locator("#name").fill("Another User")
    page.locator("#email").fill("demo@techmart.com")
    page.locator("#password").fill("password123")
    page.locator("#confirmPassword").fill("password123")
    page.locator('button[type="submit"]').click()
    error_message = page.locator("#errorMessage")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text(re.compile("already registered|exists", re.IGNORECASE))


def test_direct_url_access_to_cart_page(page):
    page.goto(f"{BASE_URL}/cart.html")
    expect(page.locator(".logo")).to_be_visible()


def test_cart_persists_across_navigation(page):
    page.locator(".add-to-cart-btn").first.click()
    page.wait_for_timeout(500)
    page.goto(f"{BASE_URL}/login.html")
    page.goto(BASE_URL)
    expect(page.locator("#cartCount").first).to_have_text("1")
