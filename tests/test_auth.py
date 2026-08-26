import time
from playwright.sync_api import expect

BASE_URL = "http://localhost:3000"

def test_login_valid_credentials(page):
    page.goto(f"{BASE_URL}/login.html")
    page.locator("#email").fill("demo@techmart.com")
    page.locator("#password").fill("demo123")
    page.locator('button[type="submit"]').click()
    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.locator("#authArea")).to_contain_text("Demo User")


def test_login_invalid_credentials(page):
    page.goto(f"{BASE_URL}/login.html")
    page.locator("#email").fill("demo@techmart.com")
    page.locator("#password").fill("wrongpassword")
    page.locator('button[type="submit"]').click()
    expect(page.locator("#errorMessage")).to_contain_text("Invalid credentials")
    expect(page).to_have_url(f"{BASE_URL}/login.html")


def test_register_new_account(page):
    unique_email = f"test{int(time.time())}@example.com"
    page.goto(f"{BASE_URL}/register.html")
    page.locator("#name").fill("Test User")
    page.locator("#email").fill(unique_email)
    page.locator("#password").fill("password123")
    page.locator("#confirmPassword").fill("password123")
    page.locator('button[type="submit"]').click()
    expect(page).to_have_url(f"{BASE_URL}/")


def test_register_password_mismatch(page):
    page.goto(f"{BASE_URL}/register.html")
    page.locator("#name").fill("Test User")
    page.locator("#email").fill("mismatch@example.com")
    page.locator("#password").fill("password123")
    page.locator("#confirmPassword").fill("different456")
    page.locator('button[type="submit"]').click()
    expect(page.locator("#errorMessage")).to_contain_text("do not match")


def test_logout(page):
    page.goto(f"{BASE_URL}/login.html")
    page.locator("#email").fill("demo@techmart.com")
    page.locator("#password").fill("demo123")
    page.locator('button[type="submit"]').click()
    expect(page.locator("#authArea")).to_contain_text("Demo User")
    page.locator("#logoutBtn").click()
    expect(page.locator("#authArea")).not_to_contain_text("Demo User")