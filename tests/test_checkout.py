from playwright.sync_api import expect

BASE_URL = "http://localhost:3000"


def setup_cart_with_one_item(page):
    page.request.delete(f"{BASE_URL}/api/cart")
    page.request.post(f"{BASE_URL}/api/cart", data={"productId": 1, "quantity": 1})


def test_redirects_to_cart_if_empty(page):
    page.request.delete(f"{BASE_URL}/api/cart")
    page.goto(f"{BASE_URL}/checkout.html")
    page.wait_for_url(f"{BASE_URL}/cart.html")


def test_checkout_form_displayed(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    for field_id in ["firstName", "lastName", "address", "city", "state", "zip",
                      "phone", "cardName", "cardNumber", "expiry", "cvv"]:
        expect(page.locator(f"#{field_id}")).to_be_visible()


def test_order_summary_displayed(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    order_summary = page.locator(".order-summary-sidebar")
    expect(order_summary).to_be_visible()
    expect(order_summary.locator(".order-item")).to_have_count(1)
    expect(page.locator("#subtotal")).to_be_visible()
    expect(page.locator("#tax")).to_be_visible()
    expect(page.locator("#total")).to_be_visible()


def test_card_number_formats_with_spaces(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    card_number = page.locator("#cardNumber")
    card_number.fill("1234567890123456")
    expect(card_number).to_have_value("1234 5678 9012 3456")


def test_expiry_date_formats_correctly(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    expiry = page.locator("#expiry")
    expiry.fill("1225")
    expect(expiry).to_have_value("12/25")


def test_complete_checkout_successfully(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")
    page.locator("#address").fill("123 Main Street")
    page.locator("#city").fill("Grand Rapids")
    page.locator("#state").select_option("MI")
    page.locator("#zip").fill("49501")
    page.locator("#phone").fill("555-123-4567")
    page.locator("#cardName").fill("John Doe")
    page.locator("#cardNumber").fill("4111111111111111")
    page.locator("#expiry").fill("12/25")
    page.locator("#cvv").fill("123")
    page.locator("#placeOrderBtn").click()
    confirmation = page.locator("#orderConfirmation")
    expect(confirmation).to_be_visible()
    expect(confirmation).to_contain_text("Order Confirmed")
    expect(page.locator("#orderId")).not_to_be_empty()


def test_required_fields_validation(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    page.locator("#placeOrderBtn").click()
    is_invalid = page.locator("#firstName").evaluate("el => !el.checkValidity()")
    assert is_invalid is True


def test_zip_code_format_validation(page):
    setup_cart_with_one_item(page)
    page.goto(f"{BASE_URL}/checkout.html")
    page.locator("#firstName").fill("John")
    page.locator("#lastName").fill("Doe")
    page.locator("#address").fill("123 Main Street")
    page.locator("#city").fill("Grand Rapids")
    page.locator("#state").select_option("MI")
    page.locator("#zip").fill("abc")
    page.locator("#phone").fill("555-123-4567")
    page.locator("#placeOrderBtn").click()
    is_invalid = page.locator("#zip").evaluate("el => !el.checkValidity()")
    assert is_invalid is True
