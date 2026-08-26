from playwright.sync_api import expect

def test_homepage_loads(page):
    page.goto("http://localhost:3000")
    expect(page).to_have_title("TechMart - Your Tech Essentials Store ")
    
def test_welcome_heading_visible(page):
    page.goto("http://localhost:3000")
    welcome_heading = page.locator("h1")
    expect(welcome_heading).to_be_visible()
    expect(welcome_heading).to_have_text("Welcome to TechMart")
    
def test_shows_six_products(page):
    page.goto("http://localhost:3000")
    expect(page.locator(".product-card")).to_have_count(6)